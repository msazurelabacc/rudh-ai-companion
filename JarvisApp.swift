// PHASE 7.2: MOBILE JARVIS KINGDOM - iOS App
// JarvisApp.swift - Your AI Companion in Your Pocket

import SwiftUI
import Foundation
import AVFoundation
import Speech
import Combine

// MARK: - Main App Structure
@main
struct JarvisApp: App {
    @StateObject private var jarvisManager = JarvisManager()
    
    var body: some Scene {
        WindowGroup {
            ContentView()
                .environmentObject(jarvisManager)
                .preferredColorScheme(.dark)
        }
    }
}

// MARK: - JARVIS Manager (Core AI System)
class JarvisManager: ObservableObject {
    @Published var isListening = false
    @Published var isProcessing = false
    @Published var currentMessage = ""
    @Published var conversationHistory: [Message] = []
    @Published var voiceEnabled = true
    @Published var connectionStatus: ConnectionStatus = .disconnected
    @Published var userProfile = UserProfile()
    
    private var speechRecognizer = SFSpeechRecognizer(locale: Locale(identifier: "en-IN"))
    private var speechSynthesizer = AVSpeechSynthesizer()
    private var audioEngine = AVAudioEngine()
    private var recognitionRequest: SFSpeechAudioBufferRecognitionRequest?
    private var recognitionTask: SFSpeechRecognitionTask?
    
    // Azure Configuration
    private let azureEndpoint = "YOUR_AZURE_ENDPOINT"
    private let azureKey = "YOUR_AZURE_KEY"
    private let speechKey = "YOUR_SPEECH_KEY"
    private let speechRegion = "southeastasia"
    
    init() {
        setupAudio()
        requestPermissions()
    }
    
    // MARK: - Voice Recognition Setup
    private func setupAudio() {
        do {
            let audioSession = AVAudioSession.sharedInstance()
            try audioSession.setCategory(.playAndRecord, mode: .measurement, options: .duckOthers)
            try audioSession.setActive(true, options: .notifyOthersOnDeactivation)
        } catch {
            print("Audio setup failed: \(error)")
        }
    }
    
    private func requestPermissions() {
        SFSpeechRecognizer.requestAuthorization { authStatus in
            DispatchQueue.main.async {
                switch authStatus {
                case .authorized:
                    self.connectionStatus = .connected
                case .denied, .restricted, .notDetermined:
                    self.connectionStatus = .error("Speech recognition not authorized")
                @unknown default:
                    break
                }
            }
        }
    }
    
    // MARK: - Voice Interaction
    func startListening() {
        guard !isListening else { return }
        
        isListening = true
        
        // Cancel previous task
        recognitionTask?.cancel()
        recognitionTask = nil
        
        // Create recognition request
        recognitionRequest = SFSpeechAudioBufferRecognitionRequest()
        guard let recognitionRequest = recognitionRequest else { return }
        
        recognitionRequest.shouldReportPartialResults = true
        
        // Create recognition task
        recognitionTask = speechRecognizer?.recognitionTask(with: recognitionRequest) { [weak self] result, error in
            guard let self = self else { return }
            
            if let result = result {
                DispatchQueue.main.async {
                    self.currentMessage = result.bestTranscription.formattedString
                }
                
                if result.isFinal {
                    self.processVoiceInput(result.bestTranscription.formattedString)
                }
            }
            
            if error != nil {
                self.stopListening()
            }
        }
        
        // Start audio recording
        let inputNode = audioEngine.inputNode
        let recordingFormat = inputNode.outputFormat(forBus: 0)
        
        inputNode.installTap(onBus: 0, bufferSize: 1024, format: recordingFormat) { buffer, _ in
            recognitionRequest.append(buffer)
        }
        
        audioEngine.prepare()
        
        do {
            try audioEngine.start()
        } catch {
            stopListening()
        }
    }
    
    func stopListening() {
        isListening = false
        audioEngine.stop()
        audioEngine.inputNode.removeTap(onBus: 0)
        recognitionRequest?.endAudio()
        recognitionRequest = nil
        recognitionTask?.cancel()
        recognitionTask = nil
    }
    
    // MARK: - AI Processing
    func processVoiceInput(_ text: String) {
        stopListening()
        processMessage(text, isVoice: true)
    }
    
    func processMessage(_ text: String, isVoice: Bool = false) {
        guard !text.isEmpty else { return }
        
        isProcessing = true
        
        // Add user message
        let userMessage = Message(
            content: text,
            isUser: true,
            timestamp: Date(),
            emotion: detectEmotion(text),
            isVoice: isVoice
        )
        conversationHistory.append(userMessage)
        
        // Generate AI response
        Task {
            do {
                let response = try await generateJarvisResponse(text)
                
                DispatchQueue.main.async {
                    let aiMessage = Message(
                        content: response.text,
                        isUser: false,
                        timestamp: Date(),
                        emotion: response.emotion,
                        confidence: response.confidence
                    )
                    self.conversationHistory.append(aiMessage)
                    
                    // Speak response if voice is enabled
                    if self.voiceEnabled {
                        self.speakText(response.text, emotion: response.emotion)
                    }
                    
                    self.isProcessing = false
                }
            } catch {
                DispatchQueue.main.async {
                    self.isProcessing = false
                    let errorMessage = Message(
                        content: "I apologize, but I encountered an error. Please try again.",
                        isUser: false,
                        timestamp: Date(),
                        emotion: "apologetic"
                    )
                    self.conversationHistory.append(errorMessage)
                }
            }
        }
    }
    
    // MARK: - Text-to-Speech
    func speakText(_ text: String, emotion: String = "neutral") {
        let utterance = AVSpeechUtterance(string: text)
        
        // Configure voice for Indian English
        if let voice = AVSpeechSynthesisVoice(identifier: "com.apple.ttsbundle.Veena-compact") ??
                      AVSpeechSynthesisVoice(language: "en-IN") {
            utterance.voice = voice
        }
        
        // Emotional styling
        switch emotion {
        case "excited", "happy":
            utterance.rate = 0.55
            utterance.pitchMultiplier = 1.1
        case "sad", "concerned":
            utterance.rate = 0.45
            utterance.pitchMultiplier = 0.9
        case "calm", "gentle":
            utterance.rate = 0.5
            utterance.pitchMultiplier = 1.0
        default:
            utterance.rate = 0.52
            utterance.pitchMultiplier = 1.0
        }
        
        speechSynthesizer.speak(utterance)
    }
    
    // MARK: - AI Response Generation
    func generateJarvisResponse(_ input: String) async throws -> JarvisResponse {
        // Simulate JARVIS-style response generation
        let emotion = detectEmotion(input)
        
        var responseText = ""
        var confidence = 0.95
        
        // Context-aware responses
        if input.lowercased().contains("jarvis") {
            responseText = "Yes, I'm here and fully operational. How may I assist you today?"
        } else if input.lowercased().contains("weather") {
            responseText = "I'd be happy to help with weather information. Let me check the current conditions for your location."
        } else if input.lowercased().contains("project") || input.lowercased().contains("work") {
            responseText = "I'm excited to help with your project! With my enhanced capabilities, we can achieve extraordinary results together."
        } else if input.lowercased().contains("voice") {
            responseText = "My voice capabilities are fully operational. I can speak in multiple languages and adapt my tone to match the conversation context."
        } else {
            // Generate contextual response based on conversation history
            responseText = generateContextualResponse(input, emotion: emotion)
        }
        
        return JarvisResponse(
            text: responseText,
            emotion: emotion,
            confidence: confidence,
            processingTime: 0.004
        )
    }
    
    private func generateContextualResponse(_ input: String, emotion: String) -> String {
        let responses = [
            "I understand your \(emotion) energy. Let me provide a thoughtful response that addresses your needs with precision.",
            "Based on my analysis, I can offer some valuable insights about your inquiry.",
            "That's an interesting point. Let me share my perspective on this matter.",
            "I'm processing your request with my full capabilities. Here's what I recommend:",
            "Drawing from my knowledge base, I believe I can help you with this effectively."
        ]
        
        return responses.randomElement() ?? "I'm here to help you with whatever you need."
    }
    
    // MARK: - Emotion Detection
    private func detectEmotion(_ text: String) -> String {
        let textLower = text.lowercased()
        
        if textLower.contains("excited") || textLower.contains("amazing") || textLower.contains("fantastic") {
            return "excited"
        } else if textLower.contains("happy") || textLower.contains("great") || textLower.contains("wonderful") {
            return "happy"
        } else if textLower.contains("sad") || textLower.contains("disappointed") {
            return "sad"
        } else if textLower.contains("help") || textLower.contains("please") {
            return "helpful"
        } else {
            return "neutral"
        }
    }
}

// MARK: - Data Models
struct Message: Identifiable, Codable {
    let id = UUID()
    let content: String
    let isUser: Bool
    let timestamp: Date
    let emotion: String
    let confidence: Double?
    let isVoice: Bool
    
    init(content: String, isUser: Bool, timestamp: Date, emotion: String, confidence: Double? = nil, isVoice: Bool = false) {
        self.content = content
        self.isUser = isUser
        self.timestamp = timestamp
        self.emotion = emotion
        self.confidence = confidence
        self.isVoice = isVoice
    }
}

struct JarvisResponse {
    let text: String
    let emotion: String
    let confidence: Double
    let processingTime: Double
}

struct UserProfile: Codable {
    var name: String = "Sir"
    var preferredLanguage: String = "en-IN"
    var voiceEnabled: Bool = true
    var notificationsEnabled: Bool = true
    var theme: String = "dark"
}

enum ConnectionStatus {
    case connected
    case connecting
    case disconnected
    case error(String)
    
    var description: String {
        switch self {
        case .connected: return "Connected"
        case .connecting: return "Connecting..."
        case .disconnected: return "Disconnected"
        case .error(let message): return "Error: \(message)"
        }
    }
    
    var color: Color {
        switch self {
        case .connected: return .green
        case .connecting: return .yellow
        case .disconnected: return .red
        case .error: return .red
        }
    }
}

// MARK: - Main UI
struct ContentView: View {
    @EnvironmentObject var jarvis: JarvisManager
    @State private var inputText = ""
    @State private var showingSettings = false
    
    var body: some View {
        NavigationView {
            VStack(spacing: 0) {
                // Header with JARVIS branding
                headerView
                
                // Conversation area
                conversationView
                
                // Input area
                inputArea
            }
            .navigationBarHidden(true)
            .background(Color.black.edgesIgnoringSafeArea(.all))
        }
        .sheet(isPresented: $showingSettings) {
            SettingsView()
                .environmentObject(jarvis)
        }
    }
    
    private var headerView: some View {
        HStack {
            VStack(alignment: .leading) {
                HStack {
                    Image(systemName: "brain.head.profile")
                        .foregroundColor(.cyan)
                        .font(.title2)
                    
                    Text("JARVIS")
                        .font(.title2)
                        .fontWeight(.bold)
                        .foregroundColor(.cyan)
                }
                
                HStack {
                    Circle()
                        .fill(jarvis.connectionStatus.color)
                        .frame(width: 8, height: 8)
                    
                    Text(jarvis.connectionStatus.description)
                        .font(.caption)
                        .foregroundColor(.gray)
                }
            }
            
            Spacer()
            
            Button(action: { showingSettings = true }) {
                Image(systemName: "gear")
                    .foregroundColor(.cyan)
                    .font(.title2)
            }
        }
        .padding()
        .background(Color.black.opacity(0.8))
    }
    
    private var conversationView: some View {
        ScrollView {
            LazyVStack(spacing: 12) {
                ForEach(jarvis.conversationHistory) { message in
                    MessageBubble(message: message)
                }
                
                if jarvis.isProcessing {
                    HStack {
                        ProgressView()
                            .progressViewStyle(CircularProgressViewStyle(tint: .cyan))
                        Text("JARVIS is thinking...")
                            .foregroundColor(.cyan)
                            .font(.caption)
                    }
                    .padding()
                }
            }
            .padding()
        }
        .background(Color.black.opacity(0.9))
    }
    
    private var inputArea: some View {
        VStack(spacing: 12) {
            // Voice button
            Button(action: {
                if jarvis.isListening {
                    jarvis.stopListening()
                } else {
                    jarvis.startListening()
                }
            }) {
                ZStack {
                    Circle()
                        .fill(jarvis.isListening ? Color.red : Color.cyan)
                        .frame(width: 80, height: 80)
                        .scaleEffect(jarvis.isListening ? 1.1 : 1.0)
                        .animation(.easeInOut(duration: 0.5).repeatForever(autoreverses: true), value: jarvis.isListening)
                    
                    Image(systemName: jarvis.isListening ? "stop.fill" : "mic.fill")
                        .foregroundColor(.black)
                        .font(.title)
                }
            }
            
            // Text input
            HStack {
                TextField("Type your message...", text: $inputText)
                    .textFieldStyle(RoundedBorderTextFieldStyle())
                    .onSubmit {
                        sendMessage()
                    }
                
                Button(action: sendMessage) {
                    Image(systemName: "arrow.up.circle.fill")
                        .foregroundColor(.cyan)
                        .font(.title2)
                }
                .disabled(inputText.isEmpty)
            }
            
            // Current listening text
            if !jarvis.currentMessage.isEmpty && jarvis.isListening {
                Text(jarvis.currentMessage)
                    .foregroundColor(.cyan)
                    .font(.caption)
                    .padding(.horizontal)
            }
        }
        .padding()
        .background(Color.black.opacity(0.8))
    }
    
    private func sendMessage() {
        guard !inputText.isEmpty else { return }
        jarvis.processMessage(inputText)
        inputText = ""
    }
}

// MARK: - Message Bubble Component
struct MessageBubble: View {
    let message: Message
    
    var body: some View {
        HStack {
            if message.isUser {
                Spacer()
            }
            
            VStack(alignment: message.isUser ? .trailing : .leading, spacing: 4) {
                HStack {
                    if !message.isUser {
                        Image(systemName: "brain.head.profile")
                            .foregroundColor(.cyan)
                            .font(.caption)
                    }
                    
                    Text(message.isUser ? "You" : "JARVIS")
                        .font(.caption)
                        .foregroundColor(.gray)
                    
                    if message.isVoice {
                        Image(systemName: "waveform")
                            .foregroundColor(.cyan)
                            .font(.caption)
                    }
                }
                
                Text(message.content)
                    .padding(12)
                    .background(
                        message.isUser ? 
                        Color.blue.opacity(0.7) : 
                        Color.gray.opacity(0.3)
                    )
                    .foregroundColor(.white)
                    .cornerRadius(16)
                
                if let confidence = message.confidence {
                    Text("Confidence: \(Int(confidence * 100))%")
                        .font(.caption2)
                        .foregroundColor(.gray)
                }
            }
            
            if !message.isUser {
                Spacer()
            }
        }
    }
}

// MARK: - Settings View
struct SettingsView: View {
    @EnvironmentObject var jarvis: JarvisManager
    @Environment(\.presentationMode) var presentationMode
    
    var body: some View {
        NavigationView {
            Form {
                Section("Voice Settings") {
                    Toggle("Voice Output", isOn: $jarvis.voiceEnabled)
                    
                    Picker("Language", selection: $jarvis.userProfile.preferredLanguage) {
                        Text("English (India)").tag("en-IN")
                        Text("Tamil").tag("ta-IN")
                        Text("English (US)").tag("en-US")
                    }
                }
                
                Section("User Profile") {
                    TextField("Name", text: $jarvis.userProfile.name)
                    Toggle("Notifications", isOn: $jarvis.userProfile.notificationsEnabled)
                }
                
                Section("About") {
                    HStack {
                        Text("Version")
                        Spacer()
                        Text("7.1.0")
                            .foregroundColor(.gray)
                    }
                    
                    HStack {
                        Text("Build")
                        Spacer()
                        Text("Voice-Enabled JARVIS")
                            .foregroundColor(.gray)
                    }
                }
            }
            .navigationTitle("Settings")
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .navigationBarTrailing) {
                    Button("Done") {
                        presentationMode.wrappedValue.dismiss()
                    }
                }
            }
        }
    }
}
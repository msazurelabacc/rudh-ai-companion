// PHASE 7.2: MOBILE JARVIS KINGDOM - Android App
// MainActivity.kt - Your AI Companion in Your Pocket

package com.rudh.jarvis

import android.Manifest
import android.content.pm.PackageManager
import android.os.Bundle
import android.speech.RecognitionListener
import android.speech.SpeechRecognizer
import android.speech.tts.TextToSpeech
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.core.content.ContextCompat
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import kotlinx.coroutines.delay
import kotlinx.coroutines.launch
import java.util.*

// MARK: - Main Activity
class MainActivity : ComponentActivity(), TextToSpeech.OnInitListener {
    
    private lateinit var jarvisViewModel: JarvisViewModel
    private var textToSpeech: TextToSpeech? = null
    private var speechRecognizer: SpeechRecognizer? = null
    
    private val requestPermissionLauncher = registerForActivityResult(
        ActivityResultContracts.RequestPermission()
    ) { isGranted: Boolean ->
        if (isGranted) {
            jarvisViewModel.initializeSpeechRecognition()
        }
    }
    
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        
        // Initialize JARVIS ViewModel
        jarvisViewModel = JarvisViewModel()
        
        // Initialize Text-to-Speech
        textToSpeech = TextToSpeech(this, this)
        
        // Request microphone permission
        if (ContextCompat.checkSelfPermission(
                this, Manifest.permission.RECORD_AUDIO
            ) != PackageManager.PERMISSION_GRANTED
        ) {
            requestPermissionLauncher.launch(Manifest.permission.RECORD_AUDIO)
        } else {
            jarvisViewModel.initializeSpeechRecognition()
        }
        
        setContent {
            JarvisTheme {
                JarvisApp(jarvisViewModel, textToSpeech)
            }
        }
    }
    
    override fun onInit(status: Int) {
        if (status == TextToSpeech.SUCCESS) {
            textToSpeech?.let { tts ->
                val result = tts.setLanguage(Locale("en", "IN"))
                if (result == TextToSpeech.LANG_MISSING_DATA || 
                    result == TextToSpeech.LANG_NOT_SUPPORTED) {
                    // Fallback to US English
                    tts.setLanguage(Locale.US)
                }
                jarvisViewModel.setTextToSpeech(tts)
            }
        }
    }
    
    override fun onDestroy() {
        textToSpeech?.stop()
        textToSpeech?.shutdown()
        speechRecognizer?.destroy()
        super.onDestroy()
    }
}

// MARK: - JARVIS ViewModel (Core AI System)
class JarvisViewModel : ViewModel() {
    
    // UI State
    private val _uiState = mutableStateOf(JarvisUiState())
    val uiState: State<JarvisUiState> = _uiState
    
    // Speech components
    private var textToSpeech: TextToSpeech? = null
    private var speechRecognizer: SpeechRecognizer? = null
    
    // Configuration
    private val azureConfig = AzureConfig(
        endpoint = "YOUR_AZURE_ENDPOINT",
        key = "YOUR_AZURE_KEY",
        speechKey = "YOUR_SPEECH_KEY",
        region = "southeastasia"
    )
    
    fun setTextToSpeech(tts: TextToSpeech) {
        textToSpeech = tts
        updateConnectionStatus(ConnectionStatus.Connected)
    }
    
    fun initializeSpeechRecognition() {
        // Speech recognition initialization would go here
        // For brevity, we'll simulate it
        updateConnectionStatus(ConnectionStatus.Connected)
    }
    
    // MARK: - Voice Interaction
    fun startListening() {
        _uiState.value = _uiState.value.copy(isListening = true)
        
        viewModelScope.launch {
            // Simulate listening (in real implementation, use SpeechRecognizer)
            delay(3000)
            val simulatedInput = "Hello JARVIS, how are you today?"
            processVoiceInput(simulatedInput)
        }
    }
    
    fun stopListening() {
        _uiState.value = _uiState.value.copy(isListening = false, currentMessage = "")
    }
    
    private fun processVoiceInput(text: String) {
        stopListening()
        processMessage(text, isVoice = true)
    }
    
    fun processMessage(text: String, isVoice: Boolean = false) {
        if (text.isBlank()) return
        
        _uiState.value = _uiState.value.copy(isProcessing = true)
        
        // Add user message
        val userMessage = Message(
            content = text,
            isUser = true,
            timestamp = System.currentTimeMillis(),
            emotion = detectEmotion(text),
            isVoice = isVoice
        )
        
        val currentHistory = _uiState.value.conversationHistory.toMutableList()
        currentHistory.add(userMessage)
        
        _uiState.value = _uiState.value.copy(conversationHistory = currentHistory)
        
        viewModelScope.launch {
            try {
                val response = generateJarvisResponse(text)
                
                val aiMessage = Message(
                    content = response.text,
                    isUser = false,
                    timestamp = System.currentTimeMillis(),
                    emotion = response.emotion,
                    confidence = response.confidence
                )
                
                val updatedHistory = _uiState.value.conversationHistory.toMutableList()
                updatedHistory.add(errorMessage)
                
                _uiState.value = _uiState.value.copy(conversationHistory = updatedHistory)
            }
        }
    }
    
    // MARK: - Text-to-Speech
    private fun speakText(text: String, emotion: String = "neutral") {
        textToSpeech?.let { tts ->
            // Configure voice based on emotion
            when (emotion) {
                "excited", "happy" -> {
                    tts.setSpeechRate(1.1f)
                    tts.setPitch(1.1f)
                }
                "sad", "concerned" -> {
                    tts.setSpeechRate(0.9f)
                    tts.setPitch(0.9f)
                }
                "calm", "gentle" -> {
                    tts.setSpeechRate(1.0f)
                    tts.setPitch(1.0f)
                }
                else -> {
                    tts.setSpeechRate(1.0f)
                    tts.setPitch(1.0f)
                }
            }
            
            tts.speak(text, TextToSpeech.QUEUE_FLUSH, null, "jarvis_response")
        }
    }
    
    // MARK: - AI Response Generation
    private suspend fun generateJarvisResponse(input: String): JarvisResponse {
        // Simulate processing time
        delay(500)
        
        val emotion = detectEmotion(input)
        val confidence = 0.95
        
        val responseText = when {
            input.lowercase().contains("jarvis") -> {
                "Yes, I'm here and fully operational. How may I assist you today?"
            }
            input.lowercase().contains("weather") -> {
                "I'd be happy to help with weather information. Let me check the current conditions for your location."
            }
            input.lowercase().contains("project") || input.lowercase().contains("work") -> {
                "I'm excited to help with your project! With my enhanced capabilities, we can achieve extraordinary results together."
            }
            input.lowercase().contains("voice") -> {
                "My voice capabilities are fully operational. I can speak in multiple languages and adapt my tone to match the conversation context."
            }
            input.lowercase().contains("hello") || input.lowercase().contains("hi") -> {
                "Hello! It's wonderful to connect with you. I'm JARVIS, your personal AI companion, ready to assist you with superhuman intelligence and capabilities."
            }
            else -> {
                generateContextualResponse(input, emotion)
            }
        }
        
        return JarvisResponse(
            text = responseText,
            emotion = emotion,
            confidence = confidence,
            processingTime = 0.004
        )
    }
    
    private fun generateContextualResponse(input: String, emotion: String): String {
        val responses = listOf(
            "I understand your $emotion energy. Let me provide a thoughtful response that addresses your needs with precision.",
            "Based on my analysis, I can offer some valuable insights about your inquiry.",
            "That's an interesting point. Let me share my perspective on this matter.",
            "I'm processing your request with my full capabilities. Here's what I recommend:",
            "Drawing from my knowledge base, I believe I can help you with this effectively."
        )
        
        return responses.random()
    }
    
    // MARK: - Emotion Detection
    private fun detectEmotion(text: String): String {
        val textLower = text.lowercase()
        
        return when {
            textLower.contains("excited") || textLower.contains("amazing") || textLower.contains("fantastic") -> "excited"
            textLower.contains("happy") || textLower.contains("great") || textLower.contains("wonderful") -> "happy"
            textLower.contains("sad") || textLower.contains("disappointed") -> "sad"
            textLower.contains("help") || textLower.contains("please") -> "helpful"
            textLower.contains("angry") || textLower.contains("frustrated") -> "angry"
            else -> "neutral"
        }
    }
    
    // MARK: - Settings
    fun toggleVoice() {
        _uiState.value = _uiState.value.copy(voiceEnabled = !_uiState.value.voiceEnabled)
    }
    
    fun updateUserName(name: String) {
        val updatedProfile = _uiState.value.userProfile.copy(name = name)
        _uiState.value = _uiState.value.copy(userProfile = updatedProfile)
    }
    
    private fun updateConnectionStatus(status: ConnectionStatus) {
        _uiState.value = _uiState.value.copy(connectionStatus = status)
    }
}

// MARK: - Data Models
data class JarvisUiState(
    val isListening: Boolean = false,
    val isProcessing: Boolean = false,
    val currentMessage: String = "",
    val conversationHistory: List<Message> = emptyList(),
    val voiceEnabled: Boolean = true,
    val connectionStatus: ConnectionStatus = ConnectionStatus.Disconnected,
    val userProfile: UserProfile = UserProfile()
)

data class Message(
    val id: String = UUID.randomUUID().toString(),
    val content: String,
    val isUser: Boolean,
    val timestamp: Long,
    val emotion: String,
    val confidence: Double? = null,
    val isVoice: Boolean = false
)

data class JarvisResponse(
    val text: String,
    val emotion: String,
    val confidence: Double,
    val processingTime: Double
)

data class UserProfile(
    val name: String = "Sir",
    val preferredLanguage: String = "en-IN",
    val voiceEnabled: Boolean = true,
    val notificationsEnabled: Boolean = true,
    val theme: String = "dark"
)

data class AzureConfig(
    val endpoint: String,
    val key: String,
    val speechKey: String,
    val region: String
)

sealed class ConnectionStatus {
    object Connected : ConnectionStatus()
    object Connecting : ConnectionStatus()
    object Disconnected : ConnectionStatus()
    data class Error(val message: String) : ConnectionStatus()
    
    val description: String
        get() = when (this) {
            is Connected -> "Connected"
            is Connecting -> "Connecting..."
            is Disconnected -> "Disconnected"
            is Error -> "Error: $message"
        }
    
    val color: Color
        get() = when (this) {
            is Connected -> Color.Green
            is Connecting -> Color.Yellow
            is Disconnected -> Color.Red
            is Error -> Color.Red
        }
}

// MARK: - Main UI Composable
@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun JarvisApp(viewModel: JarvisViewModel, textToSpeech: TextToSpeech?) {
    val uiState by viewModel.uiState
    var inputText by remember { mutableStateOf("") }
    var showSettings by remember { mutableStateOf(false) }
    
    Column(
        modifier = Modifier
            .fillMaxSize()
            .background(Color.Black)
    ) {
        // Header
        JarvisHeader(
            connectionStatus = uiState.connectionStatus,
            onSettingsClick = { showSettings = true }
        )
        
        // Conversation Area
        LazyColumn(
            modifier = Modifier
                .weight(1f)
                .padding(16.dp),
            verticalArrangement = Arrangement.Bottom
        ) {
            items(uiState.conversationHistory) { message ->
                MessageBubble(message = message)
                Spacer(modifier = Modifier.height(8.dp))
            }
            
            if (uiState.isProcessing) {
                item {
                    Row(
                        modifier = Modifier.padding(16.dp),
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        CircularProgressIndicator(
                            modifier = Modifier.size(20.dp),
                            color = Color.Cyan
                        )
                        Spacer(modifier = Modifier.width(8.dp))
                        Text(
                            text = "JARVIS is thinking...",
                            color = Color.Cyan,
                            fontSize = 12.sp
                        )
                    }
                }
            }
        }
        
        // Input Area
        JarvisInputArea(
            inputText = inputText,
            onInputChange = { inputText = it },
            onSendMessage = {
                viewModel.processMessage(inputText)
                inputText = ""
            },
            onVoiceClick = {
                if (uiState.isListening) {
                    viewModel.stopListening()
                } else {
                    viewModel.startListening()
                }
            },
            isListening = uiState.isListening,
            currentMessage = uiState.currentMessage
        )
    }
    
    // Settings Sheet
    if (showSettings) {
        ModalBottomSheet(
            onDismissRequest = { showSettings = false }
        ) {
            SettingsContent(
                userProfile = uiState.userProfile,
                voiceEnabled = uiState.voiceEnabled,
                onToggleVoice = { viewModel.toggleVoice() },
                onUpdateUserName = { viewModel.updateUserName(it) }
            )
        }
    }
}

@Composable
fun JarvisHeader(
    connectionStatus: ConnectionStatus,
    onSettingsClick: () -> Unit
) {
    Surface(
        modifier = Modifier.fillMaxWidth(),
        color = Color.Black.copy(alpha = 0.8f)
    ) {
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .padding(16.dp),
            horizontalArrangement = Arrangement.SpaceBetween,
            verticalAlignment = Alignment.CenterVertically
        ) {
            Column {
                Row(verticalAlignment = Alignment.CenterVertically) {
                    Icon(
                        imageVector = Icons.Default.Psychology,
                        contentDescription = "JARVIS",
                        tint = Color.Cyan,
                        modifier = Modifier.size(24.dp)
                    )
                    Spacer(modifier = Modifier.width(8.dp))
                    Text(
                        text = "JARVIS",
                        color = Color.Cyan,
                        fontWeight = FontWeight.Bold,
                        fontSize = 18.sp
                    )
                }
                
                Row(
                    verticalAlignment = Alignment.CenterVertically,
                    modifier = Modifier.padding(top = 4.dp)
                ) {
                    Box(
                        modifier = Modifier
                            .size(8.dp)
                            .background(connectionStatus.color, CircleShape)
                    )
                    Spacer(modifier = Modifier.width(4.dp))
                    Text(
                        text = connectionStatus.description,
                        color = Color.Gray,
                        fontSize = 12.sp
                    )
                }
            }
            
            IconButton(onClick = onSettingsClick) {
                Icon(
                    imageVector = Icons.Default.Settings,
                    contentDescription = "Settings",
                    tint = Color.Cyan
                )
            }
        }
    }
}

@Composable
fun MessageBubble(message: Message) {
    Row(
        modifier = Modifier.fillMaxWidth(),
        horizontalArrangement = if (message.isUser) Arrangement.End else Arrangement.Start
    ) {
        if (!message.isUser) {
            Spacer(modifier = Modifier.width(8.dp))
        }
        
        Column(
            horizontalAlignment = if (message.isUser) Alignment.End else Alignment.Start
        ) {
            Row(
                verticalAlignment = Alignment.CenterVertically,
                modifier = Modifier.padding(bottom = 4.dp)
            ) {
                if (!message.isUser) {
                    Icon(
                        imageVector = Icons.Default.Psychology,
                        contentDescription = "JARVIS",
                        tint = Color.Cyan,
                        modifier = Modifier.size(12.dp)
                    )
                    Spacer(modifier = Modifier.width(4.dp))
                }
                
                Text(
                    text = if (message.isUser) "You" else "JARVIS",
                    color = Color.Gray,
                    fontSize = 12.sp
                )
                
                if (message.isVoice) {
                    Spacer(modifier = Modifier.width(4.dp))
                    Icon(
                        imageVector = Icons.Default.GraphicEq,
                        contentDescription = "Voice",
                        tint = Color.Cyan,
                        modifier = Modifier.size(12.dp)
                    )
                }
            }
            
            Surface(
                modifier = Modifier.clip(RoundedCornerShape(16.dp)),
                color = if (message.isUser) Color.Blue.copy(alpha = 0.7f) else Color.Gray.copy(alpha = 0.3f)
            ) {
                Text(
                    text = message.content,
                    color = Color.White,
                    modifier = Modifier.padding(12.dp),
                    fontSize = 14.sp
                )
            }
            
            message.confidence?.let { confidence ->
                Text(
                    text = "Confidence: ${(confidence * 100).toInt()}%",
                    color = Color.Gray,
                    fontSize = 10.sp,
                    modifier = Modifier.padding(top = 2.dp)
                )
            }
        }
        
        if (message.isUser) {
            Spacer(modifier = Modifier.width(8.dp))
        }
    }
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun JarvisInputArea(
    inputText: String,
    onInputChange: (String) -> Unit,
    onSendMessage: () -> Unit,
    onVoiceClick: () -> Unit,
    isListening: Boolean,
    currentMessage: String
) {
    Surface(
        modifier = Modifier.fillMaxWidth(),
        color = Color.Black.copy(alpha = 0.8f)
    ) {
        Column(
            modifier = Modifier.padding(16.dp),
            horizontalAlignment = Alignment.CenterHorizontally
        ) {
            // Voice Button
            FloatingActionButton(
                onClick = onVoiceClick,
                modifier = Modifier.size(80.dp),
                containerColor = if (isListening) Color.Red else Color.Cyan
            ) {
                Icon(
                    imageVector = if (isListening) Icons.Default.Stop else Icons.Default.Mic,
                    contentDescription = if (isListening) "Stop Listening" else "Start Listening",
                    tint = Color.Black,
                    modifier = Modifier.size(32.dp)
                )
            }
            
            Spacer(modifier = Modifier.height(12.dp))
            
            // Text Input
            Row(
                modifier = Modifier.fillMaxWidth(),
                verticalAlignment = Alignment.CenterVertically
            ) {
                OutlinedTextField(
                    value = inputText,
                    onValueChange = onInputChange,
                    placeholder = { Text("Type your message...", color = Color.Gray) },
                    modifier = Modifier.weight(1f),
                    colors = TextFieldDefaults.outlinedTextFieldColors(
                        focusedTextColor = Color.White,
                        unfocusedTextColor = Color.White,
                        focusedBorderColor = Color.Cyan,
                        unfocusedBorderColor = Color.Gray
                    )
                )
                
                Spacer(modifier = Modifier.width(8.dp))
                
                IconButton(
                    onClick = onSendMessage,
                    enabled = inputText.isNotBlank()
                ) {
                    Icon(
                        imageVector = Icons.Default.Send,
                        contentDescription = "Send",
                        tint = if (inputText.isNotBlank()) Color.Cyan else Color.Gray
                    )
                }
            }
            
            // Current listening text
            if (currentMessage.isNotEmpty() && isListening) {
                Text(
                    text = currentMessage,
                    color = Color.Cyan,
                    fontSize = 12.sp,
                    modifier = Modifier.padding(top = 8.dp)
                )
            }
        }
    }
}

@Composable
fun SettingsContent(
    userProfile: UserProfile,
    voiceEnabled: Boolean,
    onToggleVoice: () -> Unit,
    onUpdateUserName: (String) -> Unit
) {
    var tempUserName by remember { mutableStateOf(userProfile.name) }
    
    Column(
        modifier = Modifier
            .fillMaxWidth()
            .padding(16.dp)
    ) {
        Text(
            text = "Settings",
            fontSize = 20.sp,
            fontWeight = FontWeight.Bold,
            color = Color.White,
            modifier = Modifier.padding(bottom = 16.dp)
        )
        
        // Voice Settings
        Text(
            text = "Voice Settings",
            fontSize = 16.sp,
            fontWeight = FontWeight.Medium,
            color = Color.Cyan,
            modifier = Modifier.padding(bottom = 8.dp)
        )
        
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .padding(bottom = 16.dp),
            horizontalArrangement = Arrangement.SpaceBetween,
            verticalAlignment = Alignment.CenterVertically
        ) {
            Text("Voice Output", color = Color.White)
            Switch(
                checked = voiceEnabled,
                onCheckedChange = { onToggleVoice() },
                colors = SwitchDefaults.colors(checkedThumbColor = Color.Cyan)
            )
        }
        
        // User Profile
        Text(
            text = "User Profile",
            fontSize = 16.sp,
            fontWeight = FontWeight.Medium,
            color = Color.Cyan,
            modifier = Modifier.padding(bottom = 8.dp)
        )
        
        OutlinedTextField(
            value = tempUserName,
            onValueChange = { 
                tempUserName = it
                onUpdateUserName(it)
            },
            label = { Text("Name", color = Color.Gray) },
            modifier = Modifier.fillMaxWidth(),
            colors = TextFieldDefaults.outlinedTextFieldColors(
                focusedTextColor = Color.White,
                unfocusedTextColor = Color.White,
                focusedBorderColor = Color.Cyan,
                unfocusedBorderColor = Color.Gray
            )
        )
        
        Spacer(modifier = Modifier.height(24.dp))
        
        // About
        Text(
            text = "About",
            fontSize = 16.sp,
            fontWeight = FontWeight.Medium,
            color = Color.Cyan,
            modifier = Modifier.padding(bottom = 8.dp)
        )
        
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .padding(bottom = 8.dp),
            horizontalArrangement = Arrangement.SpaceBetween
        ) {
            Text("Version", color = Color.White)
            Text("7.2.0", color = Color.Gray)
        }
        
        Row(
            modifier = Modifier.fillMaxWidth(),
            horizontalArrangement = Arrangement.SpaceBetween
        ) {
            Text("Build", color = Color.White)
            Text("Mobile JARVIS", color = Color.Gray)
        }
        
        Spacer(modifier = Modifier.height(32.dp))
    }
}

// MARK: - Theme
@Composable
fun JarvisTheme(content: @Composable () -> Unit) {
    MaterialTheme(
        colorScheme = darkColorScheme(
            primary = Color.Cyan,
            background = Color.Black,
            surface = Color.Black,
            onPrimary = Color.Black,
            onBackground = Color.White,
            onSurface = Color.White
        ),
        content = content
    )
}datedHistory.add(aiMessage)
                
                _uiState.value = _uiState.value.copy(
                    conversationHistory = updatedHistory,
                    isProcessing = false
                )
                
                // Speak response if voice is enabled
                if (_uiState.value.voiceEnabled) {
                    speakText(response.text, response.emotion)
                }
                
            } catch (e: Exception) {
                _uiState.value = _uiState.value.copy(isProcessing = false)
                
                val errorMessage = Message(
                    content = "I apologize, but I encountered an error. Please try again.",
                    isUser = false,
                    timestamp = System.currentTimeMillis(),
                    emotion = "apologetic"
                )
                
                val updatedHistory = _uiState.value.conversationHistory.toMutableList()
                up
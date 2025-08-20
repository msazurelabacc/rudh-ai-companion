// Phase 5.2: Azure Infrastructure as Code for Rudh AI Video Studio
// Enterprise-Grade Production Deployment

@description('Environment name (dev, staging, prod)')
param environment string = 'prod'

@description('Location for all resources')
param location string = 'Southeast Asia'

@description('Unique suffix for resource names')
param uniqueSuffix string = uniqueString(resourceGroup().id)

// Variables
var appName = 'rudh-ai-video-studio'
var resourcePrefix = 'rudh-${environment}'

// Storage Account for video/audio files
resource storageAccount 'Microsoft.Storage/storageAccounts@2023-01-01' = {
  name: '${resourcePrefix}storage${uniqueSuffix}'
  location: location
  sku: {
    name: 'Standard_LRS'
  }
  kind: 'StorageV2'
  properties: {
    allowBlobPublicAccess: true
    supportsHttpsTrafficOnly: true
    minimumTlsVersion: 'TLS1_2'
    accessTier: 'Hot'
  }
  
  resource blobService 'blobServices' = {
    name: 'default'
    properties: {
      cors: {
        corsRules: [
          {
            allowedOrigins: ['*']
            allowedMethods: ['GET', 'PUT', 'POST']
            allowedHeaders: ['*']
            exposedHeaders: ['*']
            maxAgeInSeconds: 3600
          }
        ]
      }
    }
    
    resource videoContainer 'containers' = {
      name: 'videos'
      properties: {
        publicAccess: 'Blob'
      }
    }
    
    resource audioContainer 'containers' = {
      name: 'audio'
      properties: {
        publicAccess: 'Blob'
      }
    }
    
    resource assetsContainer 'containers' = {
      name: 'assets'
      properties: {
        publicAccess: 'Blob'
      }
    }
  }
}

// Cognitive Services for Speech and AI
resource speechService 'Microsoft.CognitiveServices/accounts@2023-05-01' = {
  name: '${resourcePrefix}-speech-${uniqueSuffix}'
  location: location
  sku: {
    name: 'S0'
  }
  kind: 'SpeechServices'
  properties: {
    customSubDomainName: '${resourcePrefix}-speech-${uniqueSuffix}'
    publicNetworkAccess: 'Enabled'
    disableLocalAuth: false
  }
}

// OpenAI Service (if available in region)
resource openAIService 'Microsoft.CognitiveServices/accounts@2023-05-01' = {
  name: '${resourcePrefix}-openai-${uniqueSuffix}'
  location: 'East US 2' // OpenAI might not be available in Southeast Asia
  sku: {
    name: 'S0'
  }
  kind: 'OpenAI'
  properties: {
    customSubDomainName: '${resourcePrefix}-openai-${uniqueSuffix}'
    publicNetworkAccess: 'Enabled'
  }
}

// Key Vault for secure configuration
resource keyVault 'Microsoft.KeyVault/vaults@2023-02-01' = {
  name: '${resourcePrefix}-kv-${uniqueSuffix}'
  location: location
  properties: {
    sku: {
      family: 'A'
      name: 'standard'
    }
    tenantId: subscription().tenantId
    enableRbacAuthorization: true
    enableSoftDelete: true
    softDeleteRetentionInDays: 90
    publicNetworkAccess: 'Enabled'
    accessPolicies: []
  }
}

// Application Insights for monitoring
resource appInsights 'Microsoft.Insights/components@2020-02-02' = {
  name: '${resourcePrefix}-insights-${uniqueSuffix}'
  location: location
  kind: 'web'
  properties: {
    Application_Type: 'web'
    RetentionInDays: 90
    IngestionMode: 'ApplicationInsights'
    publicNetworkAccessForIngestion: 'Enabled'
    publicNetworkAccessForQuery: 'Enabled'
  }
}

// Log Analytics Workspace
resource logAnalytics 'Microsoft.OperationalInsights/workspaces@2023-09-01' = {
  name: '${resourcePrefix}-logs-${uniqueSuffix}'
  location: location
  properties: {
    sku: {
      name: 'PerGB2018'
    }
    retentionInDays: 30
    publicNetworkAccessForIngestion: 'Enabled'
    publicNetworkAccessForQuery: 'Enabled'
  }
}

// App Service Plan
resource appServicePlan 'Microsoft.Web/serverfarms@2023-01-01' = {
  name: '${resourcePrefix}-plan-${uniqueSuffix}'
  location: location
  sku: {
    name: 'S1'  // Standard tier for production
    capacity: 1
  }
  kind: 'linux'
  properties: {
    reserved: true  // Required for Linux
  }
}

// App Service for Rudh AI Video Studio
resource appService 'Microsoft.Web/sites@2023-01-01' = {
  name: '${appName}-${uniqueSuffix}'
  location: location
  kind: 'app,linux'
  identity: {
    type: 'SystemAssigned'
  }
  properties: {
    serverFarmId: appServicePlan.id
    httpsOnly: true
    clientAffinityEnabled: false
    siteConfig: {
      linuxFxVersion: 'PYTHON|3.11'
      alwaysOn: true
      ftpsState: 'Disabled'
      minTlsVersion: '1.2'
      scmMinTlsVersion: '1.2'
      http20Enabled: true
      healthCheckPath: '/health'
      appSettings: [
        {
          name: 'WEBSITES_PORT'
          value: '8000'
        }
        {
          name: 'SCM_DO_BUILD_DURING_DEPLOYMENT'
          value: 'true'
        }
        {
          name: 'AZURE_KEYVAULT_URL'
          value: keyVault.properties.vaultUri
        }
        {
          name: 'AZURE_SPEECH_KEY'
          value: '@Microsoft.KeyVault(VaultName=${keyVault.name};SecretName=speech-service-key)'
        }
        {
          name: 'AZURE_SPEECH_REGION'
          value: location
        }
        {
          name: 'AZURE_OPENAI_ENDPOINT'
          value: openAIService.properties.endpoint
        }
        {
          name: 'AZURE_OPENAI_API_KEY'
          value: '@Microsoft.KeyVault(VaultName=${keyVault.name};SecretName=openai-api-key)'
        }
        {
          name: 'AZURE_STORAGE_ACCOUNT'
          value: storageAccount.name
        }
        {
          name: 'AZURE_STORAGE_CONNECTION_STRING'
          value: '@Microsoft.KeyVault(VaultName=${keyVault.name};SecretName=storage-connection-string)'
        }
        {
          name: 'APPLICATIONINSIGHTS_CONNECTION_STRING'
          value: appInsights.properties.ConnectionString
        }
        {
          name: 'WEBSITE_TIME_ZONE'
          value: 'Asia/Kolkata'
        }
      ]
    }
  }
}

// Azure SQL Database for production data
resource sqlServer 'Microsoft.Sql/servers@2023-05-01-preview' = {
  name: '${resourcePrefix}-sql-${uniqueSuffix}'
  location: location
  properties: {
    administratorLogin: 'rudhsqladmin'
    administratorLoginPassword: '@Microsoft.KeyVault(VaultName=${keyVault.name};SecretName=sql-admin-password)'
    version: '12.0'
    publicNetworkAccess: 'Enabled'
  }
  
  resource database 'databases' = {
    name: 'rudh-production-db'
    location: location
    sku: {
      name: 'S0'  // Standard tier
      tier: 'Standard'
    }
    properties: {
      collation: 'SQL_Latin1_General_CP1_CI_AS'
      maxSizeBytes: 268435456000  // 250 GB
      catalogCollation: 'SQL_Latin1_General_CP1_CI_AS'
    }
  }
  
  resource firewallRule 'firewallRules' = {
    name: 'AllowAzureServices'
    properties: {
      startIpAddress: '0.0.0.0'
      endIpAddress: '0.0.0.0'
    }
  }
}

// Redis Cache for session management
resource redisCache 'Microsoft.Cache/Redis@2023-08-01' = {
  name: '${resourcePrefix}-redis-${uniqueSuffix}'
  location: location
  properties: {
    sku: {
      name: 'Basic'
      family: 'C'
      capacity: 0
    }
    enableNonSslPort: false
    minimumTlsVersion: '1.2'
    publicNetworkAccess: 'Enabled'
  }
}

// Service Bus for async processing
resource serviceBusNamespace 'Microsoft.ServiceBus/namespaces@2022-10-01-preview' = {
  name: '${resourcePrefix}-sb-${uniqueSuffix}'
  location: location
  sku: {
    name: 'Standard'
    tier: 'Standard'
  }
  properties: {
    minimumTlsVersion: '1.2'
    publicNetworkAccess: 'Enabled'
  }
  
  resource videoProcessingQueue 'queues' = {
    name: 'video-processing'
    properties: {
      maxSizeInMegabytes: 1024
      defaultMessageTimeToLive: 'P1D'
      deadLetteringOnMessageExpiration: true
    }
  }
  
  resource notificationTopic 'topics' = {
    name: 'notifications'
    properties: {
      maxSizeInMegabytes: 1024
      defaultMessageTimeToLive: 'P1D'
    }
  }
}

// CDN Profile for global content delivery
resource cdnProfile 'Microsoft.Cdn/profiles@2023-05-01' = {
  name: '${resourcePrefix}-cdn-${uniqueSuffix}'
  location: 'Global'
  sku: {
    name: 'Standard_Microsoft'
  }
  
  resource cdnEndpoint 'endpoints' = {
    name: '${appName}-${uniqueSuffix}'
    location: 'Global'
    properties: {
      originHostHeader: '${appName}-${uniqueSuffix}.azurewebsites.net'
      isHttpAllowed: false
      isHttpsAllowed: true
      origins: [
        {
          name: 'app-service'
          properties: {
            hostName: '${appName}-${uniqueSuffix}.azurewebsites.net'
            httpsPort: 443
            httpPort: 80
          }
        }
      ]
      deliveryPolicy: {
        rules: [
          {
            name: 'CacheVideoFiles'
            order: 1
            conditions: [
              {
                name: 'UrlFileExtension'
                parameters: {
                  operator: 'Equal'
                  matchValues: ['mp4', 'wav', 'png', 'jpg']
                }
              }
            ]
            actions: [
              {
                name: 'CacheExpiration'
                parameters: {
                  cacheBehavior: 'SetIfMissing'
                  cacheType: 'All'
                  cacheDuration: 'P7D'  // 7 days
                }
              }
            ]
          }
        ]
      }
    }
  }
}

// RBAC assignments for App Service managed identity
resource keyVaultAccessPolicy 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(keyVault.id, appService.id, 'Key Vault Secrets User')
  scope: keyVault
  properties: {
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', '4633458b-17de-408a-b874-0445c86b69e6')
    principalId: appService.identity.principalId
    principalType: 'ServicePrincipal'
  }
}

resource storageAccessPolicy 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(storageAccount.id, appService.id, 'Storage Blob Data Contributor')
  scope: storageAccount
  properties: {
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', 'ba92f5b4-2d11-453d-a403-e96b0029c9fe')
    principalId: appService.identity.principalId
    principalType: 'ServicePrincipal'
  }
}

// Store secrets in Key Vault
resource speechServiceKeySecret 'Microsoft.KeyVault/vaults/secrets@2023-02-01' = {
  parent: keyVault
  name: 'speech-service-key'
  properties: {
    value: speechService.listKeys().key1
  }
}

resource openAIKeySecret 'Microsoft.KeyVault/vaults/secrets@2023-02-01' = {
  parent: keyVault
  name: 'openai-api-key'
  properties: {
    value: openAIService.listKeys().key1
  }
}

resource storageConnectionStringSecret 'Microsoft.KeyVault/vaults/secrets@2023-02-01' = {
  parent: keyVault
  name: 'storage-connection-string'
  properties: {
    value: 'DefaultEndpointsProtocol=https;AccountName=${storageAccount.name};AccountKey=${storageAccount.listKeys().keys[0].value};EndpointSuffix=core.windows.net'
  }
}

resource sqlAdminPasswordSecret 'Microsoft.KeyVault/vaults/secrets@2023-02-01' = {
  parent: keyVault
  name: 'sql-admin-password'
  properties: {
    value: 'RudhSQL2024!${uniqueSuffix}'
  }
}

resource redisPrimaryKeySecret 'Microsoft.KeyVault/vaults/secrets@2023-02-01' = {
  parent: keyVault
  name: 'redis-primary-key'
  properties: {
    value: redisCache.listKeys().primaryKey
  }
}

// Output important values
output appServiceUrl string = 'https://${appService.properties.defaultHostName}'
output cdnEndpointUrl string = 'https://${cdnProfile::cdnEndpoint.properties.hostName}'
output storageAccountName string = storageAccount.name
output keyVaultName string = keyVault.name
output sqlServerName string = sqlServer.name
output speechServiceEndpoint string = speechService.properties.endpoint
output openAIEndpoint string = openAIService.properties.endpoint
output applicationInsightsConnectionString string = appInsights.properties.ConnectionString

// Output for deployment script
output deploymentConfiguration object = {
  resourceGroup: resourceGroup().name
  appServiceName: appService.name
  storageAccount: storageAccount.name
  keyVault: keyVault.name
  sqlServer: sqlServer.name
  sqlDatabase: sqlServer::database.name
  speechService: speechService.name
  openAIService: openAIService.name
  cdnProfile: cdnProfile.name
  cdnEndpoint: cdnProfile::cdnEndpoint.name
  serviceBus: serviceBusNamespace.name
  redisCache: redisCache.name
}

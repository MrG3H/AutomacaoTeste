pipeline {
    agent any // Roda em qualquer agente disponível

    environment {
        // Define a variável 'CRASHKEN_SECRET'
        // 'CRASHKEN_API_KEY' é o ID do segredo que você deve criar no Jenkins
        CRASHKEN_SECRET = credentials('CRASHKEN_API_KEY')
    }

    stages {
        stage('Checkout') {
            steps {
                // Clona o repositório do GitHub onde este Jenkinsfile está
                checkout scm 
            }
        }

        stage('Install Python Dependencies') {
            steps {
                // 1. Cria o ambiente virtual (venv)
                sh 'python3 -m venv venv'
                
                // 2. Ativa o venv (usando '.') e instala as libs NA MESMA LINHA
                sh '. venv/bin/activate && pip install -r requirements.txt'
            }
        }

        stage('Run Appium Test') {
            steps {
                // Bloco 'sh' de várias linhas para controlar todo o processo
                sh '''
                # Ativa o ambiente virtual
                . venv/bin/activate
                
                echo "Instalando o driver UiAutomator2 para o Appium..."
                # PASSO 1: Instala o driver necessário
                appium driver install uiautomator2
                
                echo "Iniciando servidor Appium em background (com base path /wd/hub)..."
                # PASSO 2: Inicia o Appium com a flag de compatibilidade e em background (&)
                appium --base-path /wd/hub &
                APPIUM_PID=$!
                
                echo "Esperando 10 segundos para o servidor Appium iniciar..."
                sleep 10
                
                echo "Executando o script de teste Python..."
                # PASSO 3: Roda o script Python (que agora vai encontrar o servidor)
                python3 automacaoteste.py
                PY_EXIT_CODE=$?
                
                echo "Desligando o servidor Appium (PID: $APPIUM_PID)..."
                # PASSO 4: Mata o processo do Appium para limpar o agente
                kill $APPIUM_PID
                
                # PASSO 5: Sai com o código de erro do Python (se falhou, a pipeline falha)
                exit $PY_EXIT_CODE
                '''
            }
        }
    }

    post {
        // Isso roda no final, não importa o que aconteça
        always {
            echo 'Pipeline finished.'
            // (Aqui você pode adicionar etapas para arquivar relatórios de teste)
        }
    }
}
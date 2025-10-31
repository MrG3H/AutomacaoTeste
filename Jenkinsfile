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
                // Vamos usar python3, pois o log de erro mencionou python3.12
                sh 'python3 -m venv venv'
                
                // 2. Instala as dependências USANDO o pip de dentro do venv
                // (O 'source' ativa o venv antes de rodar o pip)
                sh 'source venv/bin/activate && pip install -r requirements.txt'
            }
        }

        stage('Run Appium Test') {
            steps {
                // 3. Executa o script USANDO o python de dentro do venv
                // (O 'source' ativa o venv para que o script encontre as bibliotecas)
                sh 'source venv/bin/activate && python3 teste_calculadora.py'
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
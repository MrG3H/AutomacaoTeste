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
                // Instala as bibliotecas listadas no requirements.txt
                sh 'pip3 install -r requirements.txt'  // <-- MUDANÇA AQUI
            }
        }

        stage('Run Appium Test') {
            steps {
                // Executa seu script Python
                sh 'python3 teste_calculadora.py' // <-- MUDANÇA AQUI
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
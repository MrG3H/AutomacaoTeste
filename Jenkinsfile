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
        sh '''
        # Ativa o ambiente virtual
        . venv/bin/activate
        
        echo "Iniciando servidor Appium em background..."
        # Inicia o Appium em background e armazena o ID do processo (PID)
        appium &
        APPIUM_PID=$!
        
        # Espera 10 segundos para o servidor Appium iniciar completamente
        sleep 10
        
        echo "Executando o script de teste Python..."
        # Executa o teste. O '|| true' é um truque para garantir
        # que o script de cleanup (abaixo) rode mesmo se o Python falhar
        python3 automacaoteste.py
        
        # Salva o código de saída do Python
        PY_EXIT_CODE=$?
        
        echo "Desligando o servidor Appium (PID: $APPIUM_PID)..."
        # Mata o processo do Appium para não deixar lixo
        kill $APPIUM_PID
        
        # Sai do 'sh' com o código de erro original do Python
        # Se PY_EXIT_CODE for 0 (sucesso), a pipeline continua
        # Se for 1 (erro), a pipeline falha (como deveria)
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
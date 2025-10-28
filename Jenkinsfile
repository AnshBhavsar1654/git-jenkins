pipeline{
    agent{
	label ‘local’
    stages{
        stage('Checkout Code') {
            steps {
                git branch: 'main', url: file:///C:/Data/Nirma/Sem-7/MLOps/Jenkins/Github/demo_project
            }
        }
        stage('Show workspace'){
            steps{
                bat 'cd'
            }
        }
        stage('Build Images'){
            steps{
                bat 'docker-compose build'
            }
        }
        stage('Run Containers'){
            steps{
                bat 'docker-compose up -d'
            }
        }
    }
}
pipeline {
    agent any

    stages {
        stage('Deploy') {
            steps {
                sh 'echo "Deploying..."'
                sh 'not-a-real-command' 
            }
        }
    }

    post {
        failure {
            mail to: "ikram2121ali@gmail.com, groupmember1@example.com, groupmember2@example.com", 
                 subject: "Failed Deployment", 
                 body: "${env.BUILD_URL}"
        }
    }
}

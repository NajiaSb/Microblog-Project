pipeline {
    agent any
     environment {
       CONTAINER_NAME = "microblog"
       IMAGE_NAME = "microblogapp"
       JOB_NAME = "Microblog App"
       BUILD_URL = "http://54.173.6.81:5000/"
    }

    stages {
        stage('Checkout') {
           steps {
               checkout([$class: 'GitSCM', branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[url:'git@github.com:NajiaSb/Microblog-Project.git']]])
           }
       }
        stage('Build') {
            steps {
                echo 'Building..'
                sh 'sudo docker build --tag $IMAGE_NAME .'
            }
        }
        stage('Test') {
            steps {
                echo 'Testing..'
            }
        }
        stage('Deploy') {
            steps {
                echo 'Deploying....'
                sh 'sudo docker stop $CONTAINER_NAME || true'
                sh 'sudo docker rm $CONTAINER_NAME || true'
                sh 'sudo docker run -d -p 5000:5000 --name $CONTAINER_NAME $IMAGE_NAME'
            }
        }
    }
    post {  
         always {  
             echo 'Microblog is running ...'  
         }  
         success {  
             echo 'Microblog is running successfully ...'  
         }
        failure {
    echo "Build Failed!"
    sh "curl -X POST -H 'Content-type: application/json' --data '{\"text\":\"The job ${env.JOB_NAME} with build number ${env.BUILD_NUMBER} failed. \
    See ${env.BUILD_URL} for details.\"}' https://hooks.slack.com/services/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"
}


     }  
}

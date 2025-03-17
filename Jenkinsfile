pipeline{
	agent any
   environment {
        DOCKER_CREDENTIALS = credentials('docker-username') 
    }
   stages{
	 stage('Clone Repository') {
            steps {
		// github-pat: is the ID of my github Credentials in Jenkins.
                git credentialsId: 'github-pat', url: 'https://github.com/WalaaHijazi1/DevOps_Advance_Project.git', branch: 'main'
            }
        }
	 stage('Pull ChromeDriver Image') {
            steps {
                script {
                    // Pull the Docker image from the private registry
                    sh 'docker login -u $DOCKER_CREDENTIALS_USR -p $DOCKER_CREDENTIALS_PSW private-registry-url'
                    sh 'docker pull walaahij/chromedriver:latest'
                }
            }
        }
	stage('Run ChromeDriver Container') {
            steps {
                script {
                    // Run the ChromeDriver container and bind its port to 127.0.0.1:5000
                    sh 'docker run -d -p 127.0.0.1:5000:5000 walaahij/chromedriver:latest'
                }
            }
        }
        stage('Run Tests') {
            steps {
                script {
                    // Run tests inside the ChromeDriver Docker container
                    sh 'docker run --rm private-registry-url/chromedriver:latest your-test-command'
                }
            }
        }
          stage('Run rest_app.py') {
    	     steps {
        	sh '''
        . .myenv/bin/activate
        nohup python3 rest_app.py &
        '''
    		}
	}
	stage('Run Web_app.py'){
            steps{
                sh'''
                . .myenv/bin/activate
                nohup python3 web_app.py &
                '''
           }
        }
        stage('Run backend_testing.py'){
            steps{
                sh'''
                . .myenv/bin/activate
                python3 backend_testing.py
                '''
           }
        }
        stage('Run frontend_testing.py'){
            steps{
		 sh '''
                   docker run --rm -v $(pwd):/tests walaahij/chromedriver:latest \
                   python3 frontend_testing.py
                    '''
           }
        }
        stage('Run combined_testing.py'){
            steps{
		 sh '''
                   docker run --rm -v $(pwd):/tests walaahij/chromedriver:latest \
                   python3 combined_testing.py
                    '''
           }
        }
}
}

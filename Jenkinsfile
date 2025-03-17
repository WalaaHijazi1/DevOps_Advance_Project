pipeline{
	agent any
   stages{
	 stage('Clone Repository') {
            steps {
		// github-pat: is the ID of my github Credentials in Jenkins.
                git credentialsId: 'github-pat', url: 'https://github.com/WalaaHijazi1/DevOps_Advance_Project.git', branch: 'main'
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
                python3 web_app.py
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
                sh'''
                . .myenv/bin/activate
                python3 frontend_testing.py
                '''
           }
        }
        stage('Run combined_testing.py'){
            steps{
                sh'''
                . .myenv/bin/activate
                python3 combined_testing.py
                '''
           }
        }
}
}

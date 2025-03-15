pipeline{
	agent any
   stages{
	 stage('Clone Repository') {
            steps {
		// github-pat: is the ID of my github Credentials in Jenkins.
                git credentialsId: 'github-pat', url: 'https://github.com/WalaaHijazi1/selenium-test-jenkins.git', branch: 'main'
            }
        }

}

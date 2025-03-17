pipeline {
    agent any

    environment {
        DOCKER_CREDENTIALS = credentials('docker-username')
    }

    stages {
        stage('Clone Repository') {
            steps {
                // github-pat: is the ID of my GitHub Credentials in Jenkins.
                git credentialsId: 'github-pat', url: 'https://github.com/WalaaHijazi1/DevOps_Advance_Project.git', branch: 'main'
            }
        }

	stage('Pull ChromeDriver Image') {
            steps {
        	script {
            		try {
               		 // Ensure credentials are available
               		 echo "Docker username: $DOCKER_CREDENTIALS_USR"

                	// Log in to Docker
               		sh 'echo $DOCKER_CREDENTIALS_PSW | docker login -u $DOCKER_CREDENTIALS_USR --password-stdin'

                	// Pull the Docker image from Docker Hub
                	echo "Pulling Docker image..."
                	sh 'docker pull docker.io/walaahij/chromedriver:latest'
           		 } catch (Exception e) {
               		 error "Failed to pull Docker image: ${e.getMessage()}"
           		 }
       		 }
   		 }
	}

	stage('Run ChromeDriver Container') {
            steps {
       		 script {
            		try {
                	// Check if port 5000 is already in use
                	def portInUse = sh(script: "sudo lsof -i :5000", returnStatus: true)
                	if (portInUse == 0) {
                    		error "Port 5000 is already in use. Please ensure no other service is using this port."
              		  }	

             		   // Run the ChromeDriver container
                	echo "Running the ChromeDriver container..."
                	sh 'docker run -d -p 127.0.0.1:5000:5000 --name chromedriver-container walaahij/chromedriver:latest'

                	// Verify if the container is running
                	sh 'docker ps -a'

                	// Optional: Show logs of the container for debugging
                	sh 'docker logs $(docker ps -q --filter "name=chromedriver-container")'
            		} catch (Exception e) {
              		 error "Failed to run the ChromeDriver container: ${e.getMessage()}"
            			}
			 }
  		 }
	}
       // stage('Pull ChromeDriver Image') {
           // steps {
              //  script {
                    // Pull the Docker image from the private registry
              //      sh 'echo $DOCKER_CREDENTIALS_PSW | docker login -u $DOCKER_CREDENTIALS_USR --password-stdin'
         //           sh 'docker pull docker.io/walaahij/chromedriver:latest'
            //    }
         //   }
     //   }

        //stage('Run ChromeDriver Container') {
           // steps {
                //script {
                    // Run the ChromeDriver container and bind its port to 127.0.0.1:5000
                    // sh 'docker run -d -p 0.0.0.0:5000:5000 walaahij/chromedriver:latest'
	//	    sh 'docker run -d -p 127.0.0.1:5000:5000 walaahij/chromedriver:latest'
              //  }
           // }
        //}

	stage('Clone or Update Tests from GitHub') {
    	    steps {
        	sh '''
        	# Check if the /tests_repo directory exists inside the container
        	docker exec chromedriver-container bash -c "if [ -d /tests_repo ]; then echo 'Directory exists. Removing and cloning the repository.'; rm -rf /tests_repo; fi"
        
        	# Cloning the repository
        	docker exec chromedriver-container git clone -b main https://github.com/WalaaHijazi1/DevOps_Advance_Project.git /tests_repo

        	# Remove any existing test files in /tests to ensure overwriting
        	docker exec chromedriver-container rm -f /tests/frontend_testing.py
        	docker exec chromedriver-container rm -f /tests/combined_testing.py

        	# Copy the new test files into the /tests directory
        	docker exec chromedriver-container cp /tests_repo/frontend_testing.py /tests/
       		docker exec chromedriver-container cp /tests_repo/combined_testing.py /tests/
       		 '''
   		 }
	}

        stage('Install Dependencies') {
            steps {
                sh '''
                # Install requirements inside the container from the cloned repo
                docker exec chromedriver-container pip install --no-cache-dir --upgrade -r /tests_repo/requirements.txt
                '''
            }
        }

        stage('Run rest_app.py') {
    	steps {
	        sh '''
        	docker exec chromedriver-container bash -c "
        		cd /tests_repo && . .myenv/bin/activate && nohup python3 rest_app.py &"
        '''
    		}
	}
        stage('Run web_app.py') {
            steps {
                sh '''
                . .myenv/bin/activate
                nohup python3 web_app.py &
                '''
            }
        }

        stage('Run backend_testing.py') {
            steps {
                sh '''
                . .myenv/bin/activate
                python3 backend_testing.py
                '''
            }
        }

        stage('Run combined_testing.py') {
            steps {
                sh 'docker exec chromedriver-container python3 /tests/combined_testing.py'
            }
        }

        stage('Run frontend_testing.py') {
            steps {
                sh 'docker exec chromedriver-container python3 /tests/frontend_testing.py'
            }
        }

    }
}


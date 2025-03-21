pipeline {
    agent any

    environment {
        DOCKER_CREDENTIALS = credentials('docker-username')
    }

   stages {
        stage('Clone Repository') {
            steps {
                // GitHub credentials for repository cloning
                git credentialsId: 'github-pat', url: 'https://github.com/WalaaHijazi1/DevOps_Advance_Project.git', branch: 'main'
            }
        }
        stage('Pull ChromeDriver Image') {
            steps {
                script {
                    def imageExists = sh(script: "docker images -q walaahij/chromedriver:latest", returnStdout: true).trim()
                    if (imageExists) {
                        echo "Image already exists. Skipping pull."
                    } else {
                        echo "Image not found. Pulling from Docker Hub..."
                        sh 'echo $DOCKER_CREDENTIALS_PSW | docker login -u $DOCKER_CREDENTIALS_USR --password-stdin'
                        sh 'docker pull docker.io/walaahij/chromedriver:latest'
                    }
                }
            }
        }

        stage('Run ChromeDriver Container') {
            steps {
                script {
                    sh '''
                        if [ $(docker ps -q -f name=chromedriver) ]; then
                            echo "Container is already running."
                        elif [ $(docker ps -aq -f name=chromedriver) ]; then
                            echo "Container exists but is stopped. Restarting it..."
                            docker start chromedriver
                        else
                            echo "Container does not exist. Creating a new one..."
                            docker run -d --name chromedriver -p 127.0.0.1:5000:5005 walaahij/chromedriver:latest
                        fi
                    '''
                }
            }
        }

        stage('Clone or Update Tests from GitHub') {
            steps {
                sh '''
                    # Check if the /tests_repo directory exists inside the container
                    docker exec chromedriver bash -c "if [ -d /tests_repo ]; then echo 'Directory exists. Removing and cloning the repository.'; rm -rf /tests_repo; fi"

                    # Cloning the repository
                    docker exec chromedriver git clone -b main https://github.com/WalaaHijazi1/DevOps_Advance_Project.git /tests_repo

                    # Remove any existing test files in /tests to ensure overwriting
                    docker exec chromedriver rm -f /tests/frontend_testing.py
                    docker exec chromedriver rm -f /tests/combined_testing.py

                    # Copy the new test files into the /tests directory
                    docker exec chromedriver cp /tests_repo/frontend_testing.py /tests/
                    docker exec chromedriver cp /tests_repo/combined_testing.py /tests/
                '''
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                    # Install requirements inside the container from the cloned repo
                    docker exec chromedriver pip install --no-cache-dir --upgrade -r /tests_repo/requirements.txt
                '''
            }
        }

        //stage('Run rest_app.py') {
            //steps {
                //sh '''
                   // . .myenv/bin/activate
                    //nohup python3 rest_app.py &  # Start rest_app.py in the background
                   // # Wait for the service to be available (optional)
                    //sleep 5  # You might adjust this time or replace it with a more robust wait check
                //'''
            //}
        //}
        stage('Run rest_app.py') {
            steps {
                sh '''
            	      . .myenv/bin/activate
            	      nohup python3 rest_app.py &  # Start rest_app.py in the background
            
             	     # Wait for the backend service to be available (check every 2 seconds for up to 30 seconds)
            	     counter=0
            	     while ! curl -s 127.0.0.1:5000 > /dev/null && [ $counter -lt 15 ]; do
                	echo "Waiting for backend to be available..."
                	sleep 2
                	counter=$((counter + 1))
                   done
            
            	     if [ $counter -eq 15 ]; then
                	echo "Backend did not start in time."
                	exit 1
            	     fi
                    echo "Backend is up and running."
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
                sh 'docker exec chromedriver python3 /tests/combined_testing.py'
            }
        }

        stage('Run frontend_testing.py') {
            steps {
                sh 'docker exec chromedriver python3 /tests/frontend_testing.py'
            }
        }
    }
}

pipeline {
    agent any

    stages {

        // =========================================================
        // 1. CHECKOUT CODE FROM GITHUB
        // =========================================================
        stage('Checkout') {
            steps {
                echo '===== Checking out GitHub repository ====='

                checkout scm
            }
        }


        // =========================================================
        // 2. CHECK ENVIRONMENT
        // =========================================================
        stage('Environment Check') {
            steps {
                sh '''
                    echo "======================================"
                    echo "        ENVIRONMENT CHECK"
                    echo "======================================"

                    echo "Java:"
                    java --version

                    echo ""
                    echo "Python:"
                    python3 --version

                    echo ""
                    echo "Git:"
                    git --version

                    echo ""
                    echo "Current Directory:"
                    pwd

                    echo ""
                    echo "Repository Files:"
                    ls -la
                '''
            }
        }


        // =========================================================
        // 3. CREATE PYTHON VIRTUAL ENVIRONMENT
        // =========================================================
        stage('Setup Virtual Environment') {
            steps {
                sh '''
                    echo "======================================"
                    echo "     SETTING UP PYTHON VENV"
                    echo "======================================"

                    if [ ! -d "venv" ]; then
                        echo "venv does not exist."
                        echo "Creating new virtual environment..."

                        python3 -m venv venv
                    else
                        echo "venv already exists."
                        echo "Using existing virtual environment."
                    fi

                    echo ""
                    echo "Python inside venv:"
                    ./venv/bin/python --version

                    echo ""
                    echo "Pip inside venv:"
                    ./venv/bin/pip --version
                '''
            }
        }


        // =========================================================
        // 4. INSTALL PYTHON DEPENDENCIES
        // =========================================================
        stage('Install Requirements') {
            steps {
                sh '''
                    echo "======================================"
                    echo "       INSTALLING REQUIREMENTS"
                    echo "======================================"

                    if [ -f "requirements.txt" ]; then

                        echo "requirements.txt found."

                        ./venv/bin/python -m pip install --upgrade pip

                        ./venv/bin/pip install -r requirements.txt

                    else

                        echo "ERROR: requirements.txt not found!"
                        exit 1

                    fi

                    echo ""
                    echo "Installed packages:"
                    ./venv/bin/pip list
                '''
            }
        }


        // =========================================================
        // 5. RUN PYTEST FRAMEWORK
        // =========================================================
        stage('Run PyTest Framework') {
            steps {
                sh '''
                    echo "======================================"
                    echo "       RUNNING PYTEST FRAMEWORK"
                    echo "======================================"

                    mkdir -p reports

                    ./venv/bin/pytest -v \
                        --junitxml=reports/test-results.xml
                '''
            }
        }


        // =========================================================
        // 6. SHOW REPORT FILES
        // =========================================================
        stage('Test Report Check') {
            steps {
                sh '''
                    echo "======================================"
                    echo "          TEST REPORT"
                    echo "======================================"

                    if [ -f "reports/test-results.xml" ]; then

                        echo "JUnit test report generated successfully."

                        ls -lh reports/

                    else

                        echo "ERROR: Test report was not generated."
                        exit 1

                    fi
                '''
            }
        }
    }


    // =============================================================
    // POST BUILD ACTIONS
    // =============================================================
    post {

        always {
            echo '======================================'
            echo '       PUBLISHING TEST RESULTS'
            echo '======================================'

            junit allowEmptyResults: true,
                  testResults: 'reports/test-results.xml'
        }


        success {
            echo '======================================'
            echo '       PYTEST EXECUTION PASSED'
            echo '======================================'
        }


        failure {
            echo '======================================'
            echo '       PYTEST EXECUTION FAILED'
            echo '======================================'

            echo 'Please check Jenkins Console Output.'
        }
    }
}

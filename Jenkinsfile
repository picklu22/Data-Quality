pipeline {

    agent any

    stages {

        // =========================================================
        // 1. CHECKOUT
        // =========================================================
        stage('Checkout') {
            steps {
                echo '======================================'
                echo '       CHECKING OUT GITHUB CODE'
                echo '======================================'

                checkout scm
            }
        }


        // =========================================================
        // 2. ENVIRONMENT CHECK
        // =========================================================
        stage('Environment Check') {
            steps {
                sh '''
                    echo "======================================"
                    echo "        ENVIRONMENT CHECK"
                    echo "======================================"

                    echo ""
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

                    echo ""
                    echo "Report Directory:"
                    if [ -d "Report" ]; then
                        ls -lah Report
                    else
                        echo "Report directory does not exist."
                    fi
                '''
            }
        }


        // =========================================================
        // 3. SETUP PYTHON VIRTUAL ENVIRONMENT
        // =========================================================
        stage('Setup Virtual Environment') {
            steps {
                sh '''
                    echo "======================================"
                    echo "     SETTING UP PYTHON VENV"
                    echo "======================================"

                    if [ -x ".venv/bin/python" ]; then

                        echo ".venv already exists."
                        echo "Using existing virtual environment."

                    else

                        echo ".venv not found."
                        echo "Creating new virtual environment..."

                        rm -rf .venv

                        python3 -m venv .venv

                    fi

                    echo ""
                    echo "Python version:"
                    ./.venv/bin/python --version

                    echo ""
                    echo "Pip version:"
                    ./.venv/bin/python -m pip --version
                '''
            }
        }


        // =========================================================
        // 4. INSTALL REQUIREMENTS
        // =========================================================
        stage('Install Requirements') {
            steps {
                sh '''
                    echo "======================================"
                    echo "       INSTALLING REQUIREMENTS"
                    echo "======================================"

                    if [ ! -f "requirements.txt" ]; then
                        echo "ERROR: requirements.txt not found."
                        exit 1
                    fi

                    ./.venv/bin/python -m pip install --upgrade pip

                    ./.venv/bin/python -m pip install -r requirements.txt

                    echo ""
                    echo "Installed packages:"
                    ./.venv/bin/python -m pip list
                '''
            }
        }


        // =========================================================
        // 5. CLEAN OLD JENKINS REPORT
        // =========================================================
        stage('Clean Jenkins Reports') {
            steps {
                sh '''
                    echo "======================================"
                    echo "       CLEANING OLD REPORTS"
                    echo "======================================"

                    rm -rf jenkins-reports

                    mkdir -p jenkins-reports

                    echo "Jenkins report directory created."
                '''
            }
        }


        // =========================================================
        // 6. RUN PYTEST
        // =========================================================
        stage('Run PyTest Framework') {
            steps {
                sh '''
                    echo "======================================"
                    echo "       RUNNING PYTEST FRAMEWORK"
                    echo "======================================"

                    ./.venv/bin/python -m pytest -v \
                        --junitxml=jenkins-reports/test-results.xml

                    echo ""
                    echo "PyTest execution completed."
                '''
            }
        }


        // =========================================================
        // 7. CHECK JUNIT REPORT
        // =========================================================
        stage('Check JUnit Report') {
            steps {
                sh '''
                    echo "======================================"
                    echo "        CHECKING JUNIT REPORT"
                    echo "======================================"

                    if [ -f "jenkins-reports/test-results.xml" ]; then

                        echo "JUnit report generated successfully."

                        ls -lh jenkins-reports/test-results.xml

                    else

                        echo "ERROR: JUnit report was not generated."

                        exit 1

                    fi
                '''
            }
        }


        // =========================================================
        // 8. CHECK HTML REPORT
        // =========================================================
        stage('Check HTML Report') {
            steps {
                sh '''
                    echo "======================================"
                    echo "        CHECKING HTML REPORT"
                    echo "======================================"

                    echo ""
                    echo "Report directory:"
                    ls -lah Report/

                    echo ""

                    if [ -f "Report/data_quality_report.html" ]; then

                        echo "SUCCESS:"
                        echo "data_quality_report.html generated."

                        ls -lh Report/data_quality_report.html

                    else

                        echo "WARNING:"
                        echo "data_quality_report.html was NOT generated."

                    fi

                    echo ""

                    if [ -f "Report/report.html" ]; then

                        echo "SUCCESS:"
                        echo "report.html generated."

                        ls -lh Report/report.html

                    else

                        echo "WARNING:"
                        echo "report.html was NOT generated."

                    fi
                '''
            }
        }
    }


    // =============================================================
    // POST BUILD
    // =============================================================
    post {

        always {

            echo '======================================'
            echo '       PUBLISHING TEST RESULTS'
            echo '======================================'


            // -----------------------------------------------------
            // JUNIT RESULTS
            // -----------------------------------------------------

            junit(
                allowEmptyResults: true,
                testResults: 'jenkins-reports/test-results.xml'
            )


            // -----------------------------------------------------
            // ARCHIVE HTML REPORTS
            // -----------------------------------------------------

            echo '======================================'
            echo '       ARCHIVING HTML REPORTS'
            echo '======================================'


            archiveArtifacts(
                artifacts: 'Report/*.html,Report/assets/**/*',
                allowEmptyArchive: true,
                fingerprint: true
            )


            // -----------------------------------------------------
            // ARCHIVE JUNIT XML
            // -----------------------------------------------------

            archiveArtifacts(
                artifacts: 'jenkins-reports/test-results.xml',
                allowEmptyArchive: true,
                fingerprint: true
            )
        }


        success {

            echo '======================================'
            echo '       PYTEST EXECUTION PASSED'
            echo '======================================'

            echo 'Build completed successfully.'
        }


        failure {

            echo '======================================'
            echo '       PYTEST EXECUTION FAILED'
            echo '======================================'

            echo 'Please check Jenkins Console Output.'
        }
    }
}

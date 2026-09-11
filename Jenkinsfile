pipeline {

    agent any

    stages {

        // =========================================================
        // 1. CHECKOUT CODE FROM GITHUB
        // =========================================================
        stage('Checkout') {
            steps {

                echo '======================================'
                echo '       CHECKING OUT GITHUB CODE'
                echo '======================================'

                checkout scm

                echo 'GitHub checkout completed.'
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
                        ls -la Report
                    else
                        echo "Report directory does not exist yet."
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

                    # Jenkins should use a Linux-compatible venv.
                    # If .venv/bin/python exists, reuse it.
                    # Otherwise create a new .venv.

                    if [ -x ".venv/bin/python" ]; then

                        echo "Existing .venv found."
                        echo "Using existing virtual environment."

                    else

                        echo ".venv is missing or not Linux-compatible."
                        echo "Creating new virtual environment..."

                        rm -rf .venv

                        python3 -m venv .venv

                    fi

                    echo ""
                    echo "Python:"
                    ./.venv/bin/python --version

                    echo ""
                    echo "Pip:"
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

                    echo "requirements.txt found."

                    ./.venv/bin/python -m pip install --upgrade pip

                    ./.venv/bin/python -m pip install -r requirements.txt

                    echo ""
                    echo "Installed packages:"
                    ./.venv/bin/python -m pip list
                '''
            }
        }


        // =========================================================
        // 5. CLEAN OLD GENERATED REPORTS
        // =========================================================
        stage('Clean Old Reports') {
            steps {

                sh '''
                    echo "======================================"
                    echo "       CLEANING OLD REPORTS"
                    echo "======================================"

                    # Keep the Report directory and assets.
                    # Remove only previously generated HTML reports.

                    mkdir -p Report

                    rm -f Report/data_quality_report.html
                    rm -f Report/report.html

                    # Create Jenkins-specific report directory
                    rm -rf jenkins-reports
                    mkdir -p jenkins-reports

                    echo ""
                    echo "Report directory after cleanup:"

                    ls -la Report

                    echo ""
                    echo "Jenkins report directory:"

                    ls -la jenkins-reports
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

                        echo ""
                        echo "File details:"
                        ls -lh jenkins-reports/test-results.xml

                        echo ""
                        echo "Report timestamp:"
                        stat jenkins-reports/test-results.xml

                        echo ""
                        echo "First 20 lines:"
                        head -20 jenkins-reports/test-results.xml

                    else

                        echo "ERROR:"
                        echo "JUnit report was NOT generated."

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

                        echo "data_quality_report.html found."

                        ls -lh Report/data_quality_report.html

                    else

                        echo "WARNING:"
                        echo "data_quality_report.html was not generated."

                    fi

                    echo ""

                    if [ -f "Report/report.html" ]; then

                        echo "report.html found."

                        ls -lh Report/report.html

                    else

                        echo "WARNING:"
                        echo "report.html was not generated."

                    fi
                '''
            }
        }
    }


    // =============================================================
    // POST BUILD ACTIONS
    // =============================================================
    post {

        // ---------------------------------------------------------
        // ALWAYS PUBLISH JUNIT RESULTS
        // ---------------------------------------------------------
        always {

            echo '======================================'
            echo '       PUBLISHING JUNIT RESULTS'
            echo '======================================'

            junit(
                allowEmptyResults: true,
                testResults: 'jenkins-reports/test-results.xml'
            )


            // -----------------------------------------------------
            // PUBLISH data_quality_report.html
            // -----------------------------------------------------
            script {

                if (fileExists('Report/data_quality_report.html')) {

                    echo 'Publishing data_quality_report.html'

                    publishHTML(
                        target: [
                            allowMissing: true,
                            alwaysLinkToLastBuild: true,
                            keepAll: true,
                            reportDir: 'Report',
                            reportFiles: 'data_quality_report.html',
                            reportName: 'Data Quality Report',
                            reportTitles: 'Data Quality Report'
                        ]
                    )

                } else {

                    echo 'data_quality_report.html not found.'
                }


                // -------------------------------------------------
                // PUBLISH report.html
                // -------------------------------------------------

                if (fileExists('Report/report.html')) {

                    echo 'Publishing report.html'

                    publishHTML(
                        target: [
                            allowMissing: true,
                            alwaysLinkToLastBuild: true,
                            keepAll: true,
                            reportDir: 'Report',
                            reportFiles: 'report.html',
                            reportName: 'Test Report',
                            reportTitles: 'Test Report'
                        ]
                    )

                } else {

                    echo 'report.html not found.'
                }
            }


            // -----------------------------------------------------
            // ARCHIVE REPORTS
            // -----------------------------------------------------

            archiveArtifacts(
                artifacts: 'Report/*.html,Report/assets/**/*,jenkins-reports/test-results.xml',
                allowEmptyArchive: true,
                fingerprint: true
            )
        }


        // ---------------------------------------------------------
        // SUCCESS
        // ---------------------------------------------------------
        success {

            echo '======================================'
            echo '       PYTEST EXECUTION PASSED'
            echo '======================================'

            echo 'Build completed successfully.'
        }


        // ---------------------------------------------------------
        // FAILURE
        // ---------------------------------------------------------
        failure {

            echo '======================================'
            echo '       PYTEST EXECUTION FAILED'
            echo '======================================'

            echo 'Please check Jenkins Console Output.'

            echo 'JUnit results and generated reports will still be published if available.'
        }
    }
}

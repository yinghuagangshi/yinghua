pipeline {
    agent any
    environment {
        // 远程服务器配置
        REMOTE_SERVER = '47.97.37.145'
        PROJECT_DIR = '/root/yinghua'
        GIT_REPO = 'https://gitee.com/yinghuagangshi/yinghua.git'
        PYTHON_CMD = '/usr/bin/python3.6'
        TEST_FILE = 'testcases/unit_tests/test_common.py'

        // 邮件配置
        EMAIL_RECIPIENTS = 'slg112511@163.com'
        EMAIL_REPLY_TO = 'shilingang111@163.com'

        // 路径配置（区分远程和本地）
        REMOTE_ALLURE_RESULTS = 'reports/allure-results'
        LOCAL_ALLURE_RESULTS = 'allure-results'
        REMOTE_JUNIT_RESULTS = 'reports/test-results.xml'
        LOCAL_JUNIT_RESULTS = 'test-results.xml'
    }

    stages {
        stage('Force Sync Code') {
            steps {
                sshagent(credentials: ['ssh_root_credentials']) {
                    sh """
                    ssh -T -o StrictHostKeyChecking=no root@${REMOTE_SERVER} '
                        set -ex
                        echo "=== 强制同步代码 ==="
                        mkdir -p ${PROJECT_DIR}
                        cd ${PROJECT_DIR}
                        if [ ! -d .git ]; then
                            git clone ${GIT_REPO} .
                        else
                            git fetch --all --prune
                            git reset --hard origin/\$(git rev-parse --abbrev-ref HEAD)
                            git clean -fd
                        fi
                        echo "代码版本: \$(git rev-parse --short HEAD)"
                    '
                    """
                }
            }
        }

        stage('Verify Environment') {
            steps {
                sshagent(credentials: ['ssh_root_credentials']) {
                    sh """
                    ssh -T -o StrictHostKeyChecking=no root@${REMOTE_SERVER} '
                        set -ex
                        echo "=== 环境验证 ==="
                        export PATH=\$PATH:/root/.local/bin
                        ${PYTHON_CMD} --version
                        ${PYTHON_CMD} -m pip list | grep -E "pytest|allure"
                    '
                    """
                }
            }
        }

        stage('Setup Dependencies') {
            steps {
                sshagent(credentials: ['ssh_root_credentials']) {
                    sh """
                    ssh -T -o StrictHostKeyChecking=no root@${REMOTE_SERVER} '
                        set -ex
                        echo "=== 安装依赖 ==="
                        cd ${PROJECT_DIR}
                        ${PYTHON_CMD} -m pip install -U pip
                        ${PYTHON_CMD} -m pip install pytest pytest-asyncio allure-pytest
                        [ -f requirements.txt ] && ${PYTHON_CMD} -m pip install -r requirements.txt
                        mkdir -p ${PROJECT_DIR}/reports
                    '
                    """
                }
            }
        }

        stage('Run Tests with Allure') {
            steps {
                sshagent(credentials: ['ssh_root_credentials']) {
                    sh """
                    ssh -T -o StrictHostKeyChecking=no root@${REMOTE_SERVER} '
                        set -ex
                        echo "=== 运行测试 ==="
                        cd ${PROJECT_DIR}
                        ${PYTHON_CMD} -m pytest ${TEST_FILE} \\
                            --junitxml=${PROJECT_DIR}/${REMOTE_JUNIT_RESULTS} \\
                            --alluredir=${PROJECT_DIR}/${REMOTE_ALLURE_RESULTS} \\
                            -v || true
                    '
                    """
                    // 拉取结果文件
                    sh """
                    scp -o StrictHostKeyChecking=no root@${REMOTE_SERVER}:${PROJECT_DIR}/${REMOTE_JUNIT_RESULTS} ${LOCAL_JUNIT_RESULTS}
                    scp -o StrictHostKeyChecking=no -r root@${REMOTE_SERVER}:${PROJECT_DIR}/${REMOTE_ALLURE_RESULTS} ${LOCAL_ALLURE_RESULTS}
                    """
                }
            }
            post {
                always {
                    junit testResults: "${LOCAL_JUNIT_RESULTS}",
                          allowEmptyResults: true,
                          skipMarkingBuildUnstable: true

                    script {
                        allure([
                            includeProperties: false,
                            jdk: '',
                            properties: [],
                            reportBuildPolicy: 'ALWAYS',
                            results: [[path: "${LOCAL_ALLURE_RESULTS}"]],
                            reportDir: 'allure-report'  // 明确指定报告目录
                        ])
                    }
                }
            }
        }
    }

    post {
        always {
            // 先归档重要文件再清理
            archiveArtifacts artifacts: "allure-report/**", allowEmptyArchive: true
            archiveArtifacts artifacts: "${LOCAL_JUNIT_RESULTS}", allowEmptyArchive: true

            // 保留最近5次构建的Allure历史
            script {
                allure([
                    results: [[path: "${LOCAL_ALLURE_RESULTS}"]],
                    reportDir: 'allure-report',
                    historyBuildLimit: 5
                ])
            }

            // 最后清理工作区
            cleanWs(
                cleanWhenAborted: true,
                cleanWhenFailure: true,
                cleanWhenNotBuilt: true,
                cleanWhenSuccess: true,
                cleanWhenUnstable: true
            )

            // 邮件通知
            emailext (
                subject: "${env.JOB_NAME} - Build #${env.BUILD_NUMBER} - ${currentBuild.currentResult}",
                body: """
                <h2>${env.JOB_NAME} 构建结果</h2>
                <p><strong>状态:</strong> <span style="color:${currentBuild.currentResult == 'SUCCESS' ? 'green' : 'red'}">${currentBuild.currentResult}</span></p>
                <p><strong>构建编号:</strong> ${env.BUILD_NUMBER}</p>
                <p><strong>测试报告:</strong> <a href="${env.BUILD_URL}allure">Allure Report</a></p>
                <p><strong>变更记录:</strong><br>
                ${currentBuild.changeSets.collect { cs -> cs.items.collect { "${it.commitId}: ${it.msg}" }.join('<br>') }.join('<br>')}
                </p>
                """,
                to: "${env.EMAIL_RECIPIENTS}",
                replyTo: "${env.EMAIL_REPLY_TO}",
                attachLog: true
            )
        }
    }
}
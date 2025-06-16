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

        // 路径配置（使用唯一构建ID避免冲突）
        BUILD_TAG = "${env.JOB_NAME}-${env.BUILD_NUMBER}".replaceAll(' ', '_')
        REMOTE_ALLURE_RESULTS = 'reports/allure-results'
        LOCAL_ALLURE_RESULTS = "allure-results-${BUILD_TAG}"
        REMOTE_JUNIT_RESULTS = 'reports/test-results.xml'
        LOCAL_JUNIT_RESULTS = "test-results-${BUILD_TAG}.xml"
        ALLURE_REPORT_DIR = "allure-report-${BUILD_TAG}"
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
                            git clean -fd -x
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
                    // 确保本地目录存在
                    sh "mkdir -p ${LOCAL_ALLURE_RESULTS}"

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
                    // 使用rsync避免重复文件问题
                    sh """
                    rsync -avz --remove-source-files \
                        -e "ssh -o StrictHostKeyChecking=no" \
                        root@${REMOTE_SERVER}:${PROJECT_DIR}/${REMOTE_ALLURE_RESULTS}/ ${LOCAL_ALLURE_RESULTS}/
                    """
                    sh """
                    scp -o StrictHostKeyChecking=no \
                        root@${REMOTE_SERVER}:${PROJECT_DIR}/${REMOTE_JUNIT_RESULTS} \
                        ${LOCAL_JUNIT_RESULTS}
                    """
                }
            }
            post {
                always {
                    junit testResults: "${LOCAL_JUNIT_RESULTS}",
                          allowEmptyResults: true,
                          skipMarkingBuildUnstable: true

                    script {
                        // 生成唯一命名的Allure报告
                        allure([
                            includeProperties: false,
                            jdk: '',
                            properties: [],
                            reportBuildPolicy: 'ALWAYS',
                            results: [[path: "${LOCAL_ALLURE_RESULTS}"]],
                            reportDir: "${ALLURE_REPORT_DIR}",
                            historyBuildLimit: 5
                        ])

                        // 压缩报告避免文件冲突
                        sh """
                            zip -qr "${ALLURE_REPORT_DIR}.zip" "${ALLURE_REPORT_DIR}"
                        """
                    }
                }
            }
        }
    }

    post {
        always {
            // 归档压缩后的报告
            archiveArtifacts artifacts: "${ALLURE_REPORT_DIR}.zip", allowEmptyArchive: true
            archiveArtifacts artifacts: "${LOCAL_JUNIT_RESULTS}", allowEmptyArchive: true

            // 安全清理工作区（保留本次构建产物）
            cleanWs(
                cleanWhenAborted: true,
                cleanWhenFailure: true,
                cleanWhenNotBuilt: true,
                cleanWhenSuccess: true,
                cleanWhenUnstable: true,
                patterns: [
                    [pattern: '**', type: 'EXCLUDE', exclude: "${ALLURE_REPORT_DIR}**"],
                    [pattern: '**', type: 'EXCLUDE', exclude: "${ALLURE_REPORT_DIR}.zip"],
                    [pattern: '**', type: 'EXCLUDE', exclude: "${LOCAL_JUNIT_RESULTS}"]
                ]
            )

            // 邮件通知（包含直接下载链接）
            emailext (
                subject: "${env.JOB_NAME} - Build #${env.BUILD_NUMBER} - ${currentBuild.currentResult}",
                body: """
                <h2>${env.JOB_NAME} 构建结果</h2>
                <p><strong>状态:</strong> <span style="color:${currentBuild.currentResult == 'SUCCESS' ? 'green' : 'red'}">${currentBuild.currentResult}</span></p>
                <p><strong>构建编号:</strong> ${env.BUILD_NUMBER}</p>
                <p><strong>测试报告:</strong>
                   <a href="${env.BUILD_URL}allure">在线查看</a> |
                   <a href="${env.BUILD_URL}artifact/${ALLURE_REPORT_DIR}.zip">下载ZIP</a>
                </p>
                <p><strong>JUnit报告:</strong> <a href="${env.BUILD_URL}artifact/${LOCAL_JUNIT_RESULTS}">查看</a></p>
                ${currentBuild.changeSets ? """
                <p><strong>变更记录:</strong><br>
                ${currentBuild.changeSets.collect { cs ->
                    cs.items.collect {
                        "• ${it.commitId.take(8)}: ${it.msg.replaceAll('<','&lt;')} (by ${it.author})"
                    }.join('<br>')
                }.join('<br>')}
                </p>
                """ : ''}
                """,
                to: "${env.EMAIL_RECIPIENTS}",
                replyTo: "${env.EMAIL_REPLY_TO}",
                attachLog: true,
                mimeType: 'text/html'
            )
        }
    }
}
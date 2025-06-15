pipeline {
    agent any

    environment {
        // 可以在这里定义环境变量
        REMOTE_SERVER = '47.97.37.145'
        PROJECT_DIR = '/root/yinghua'
    }

    stages {
        stage('Run Test on Remote Server') {
            steps {
                sshagent(credentials: ['ssh_root_credentials']) {
                    script {
                        try {
                            sh """
                            ssh -o StrictHostKeyChecking=no root@${REMOTE_SERVER} << 'ENDSSH'
                                cd ${PROJECT_DIR}
                                mkdir -p ${PROJECT_DIR}
                                git pull origin master
                                python3.6 -m pytest testcases/unit_tests/test.py --maxfail=1 --disable-warnings -q
                            ENDSSH
                            """
                        } catch (Exception e) {
                            error "远程测试执行失败: ${e.message}"
                        }
                    }
                }
            }

            post {
                always {
                    echo '测试阶段完成，清理或发送通知可以放在这里'
                }
            }
        }
    }

    post {
        success {
            echo 'Pipeline 执行成功!'
        }
        failure {
            echo 'Pipeline 执行失败!'
        }
    }
}
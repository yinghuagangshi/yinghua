pipeline {
    agent any

    stages {
        stage('Run Test on Remote Server') {
            steps {
                sshagent(credentials: ['ssh_root_credentials']) {
                    sh '''
                    ssh -o StrictHostKeyChecking=no root@47.97.37.145 << 'ENDSSH'
                        cd /root/yinghua  # 根据你克隆代码的位置修改
                        git pull origin master
                        python3.6 -m pytest testcases/unit_tests/test.py --maxfail=1 --disable-warnings -q
                    ENDSSH
                    '''
                }
            }
        }
    }
}

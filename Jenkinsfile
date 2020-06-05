node('docker-slave') {

   stage('Preparation') { // for display purposes
      // Get some code from a GitHub repository
      git 'https://github.com/sergiobaquero/test1'

   }
   stage('Build') {

      sh 'docker build -t sergiobaquero:trainingmodel .'

   }
   stage('Run') {
    withCredentials([usernamePassword(credentialsId: 'NexusUser', usernameVariable: 'USER', passwordVariable: 'PASS')]) {
      sh '''
            docker rm -f entrenamiento || true
            docker run --name entrenamiento  -v "$(pwd)":/code sergiobaquero:trainingmodel
            curl -v -u $USER:$PASS --upload-file svc.pkl http://172.31.6.60:8081/repository/maven-releases/org/svc/4.0/svc-4.0.pkl
            docker rm entrenamiento
            rm svc.pkl
            
            curl -v -u $USER:$PASS -X GET http://172.31.6.60:8081/repository/maven-releases/org/svc/4.0/svc-4.0.pkl --output svc-4.0.pkl
            mv svc-4.0.pkl svc.pkl
            docker rm -f test || true
            docker run --name test  -v "$(pwd)":/code sergiobaquero:trainingmodel python3 ./src/model/test.py
            docker rm test
            pwd
            cd $HOME
            pwd
            ls -la
            whoami
            psql -h 172.31.6.60 -U postgres -d postgres -c """INSERT INTO training VALUES (4,20201010,'NEWR','KK')"""
        '''
            
    }
   }
   stage('Results') {
       //withCredentials([usernamePassword(credentialsId: 'gituser', usernameVariable: 'USER', passwordVariable: 'PASS')]) {
        //                       script {
       //                 env.encodedPass=URLEncoder.encode(PASS, "UTF-8")
       //             }
        //sh 'curl -v -u admin:piticlines --upload-file svc.pkl http://18.184.88.67:8081/repository/maven-releases/org/svc/3.0/svc-3.0.pkl'
        //sh 'cd src/model'
        //sh 'curl -u admin:piticlines -X GET http://18.184.88.67:8081/repository/maven-releases/org/svc/3.0/svc-3.0.pkl > svc.pkl'

      // }
      //junit '**/target/surefire-reports/TEST-*.xml'
      //archiveArtifacts 'target/*.jar'
   }
}

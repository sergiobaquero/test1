node('docker-slave') {
checkout scm
   stage('Preparation') { // for display purposes
      // Get some code from a GitHub repository
      //git 'https://github.com/sergiobaquero/test1'

   }
   stage('Build') {

      sh '''
          #!/bin/bash -xe
          rm $WORKSPACE/envvars || true
          commit_user=$(git show -s --pretty=%an)
          no_blank_commit_user=$(echo "$commit_user" | tr -d "[:space:]")
          echo "commit_user=\"$no_blank_commit_user\"" >> $WORKSPACE/envvars

          echo "COMMIT USER"
          commit_user2=$(git show -s --pretty=%cn)
          echo "$commit_user2"

          echo "COMMIT email"
          commit_email=$(git show -s --pretty=%ce)
          echo "$commit_email"

          sha=$(git rev-parse HEAD)
          echo "sha=\"$sha\"" >> $WORKSPACE/envvars

          info=$(git config --list)
          echo "$info"

          docker build -t sergiobaquero:trainingmodel .
      '''

   }
   stage('Run') {
    withCredentials([usernamePassword(credentialsId: 'NexusUser', usernameVariable: 'USER', passwordVariable: 'PASS')]) {
      echo "Running ${env.BUILD_ID} on ${env.JENKINS_URL}"
      sh '''#!/bin/bash -xe

            start=`date +%s`
            . $WORKSPACE/envvars

            #git rev-parse HEAD > .commit
            #sha=`cat .commit`

            type=${BRANCH_NAME:0:3}
            if [ "$type" == 'PR-' ];
            then
               BRANCH_NAME='PR'
               echo "BRANCH_NAME=\"$BRANCH_NAME\"" >> $WORKSPACE/envvars
            fi

            docker rm -f entrenamiento || true
            docker run --name entrenamiento  -v "$(pwd)":/code sergiobaquero:trainingmodel

            model_name=`cat .model_name.txt`
            echo "model_name=\"$model_name\"" >> $WORKSPACE/envvars

            curl -v -u $USER:$PASS --upload-file $model_name.pkl http://172.31.7.247:8081/repository/models/$model_name/$BRANCH_NAME/$sha/$model_name.pkl
            docker rm entrenamiento
            rm $model_name.pkl

            end=`date +%s`
            traintime=$((end-start))
            echo "traintime=\"$traintime\"" >> $WORKSPACE/envvars


      '''
       }
    }
    stage('Test') {
     withCredentials([usernamePassword(credentialsId: 'NexusUser', usernameVariable: 'USER', passwordVariable: 'PASS')]) {
      echo "Running ${env.BUILD_ID} on ${env.JENKINS_URL}"
      sh '''#!/bin/bash -xe

            start=`date +%s`

            . $WORKSPACE/envvars

            curl -v -u $USER:$PASS -X GET http://172.31.7.247:8081/repository/models/$model_name/$BRANCH_NAME/$sha/$model_name.pkl --output $model_name.pkl

            docker rm -f test || true
            docker run --name test  -v "$(pwd)":/code sergiobaquero:trainingmodel python3 ./src/model/test.py
            docker rm test

            precision=`cat .accuracy.txt`
            echo "precision=\"$precision\"" >> $WORKSPACE/envvars

            end=`date +%s`
            testtime=$((end-start))

            echo "testtime=\"$testtime\"" >> $WORKSPACE/envvars

        '''

    }
   }
   stage('Results') {
        withCredentials([string(credentialsId: 'postgres_insert_user', variable: 'USER')]) {
            sh '''
            . $WORKSPACE/envvars

            #echo "EL USUARIOS ES:"
            #echo "$commit_user"
            #precision=`cat .accuracy.txt`
            #model_name=`cat .model_name.txt`
            #train_duration=`cat .trainduration.txt`
            #test_duration=`cat .testduration.txt`

            if [ -z "$CHANGE_AUTHOR" ];
            then
              CHANGE_AUTHOR=$commit_user
              echo "HOLA"
            fi

            psql -h 172.31.7.247 -U $USER -d postgres -c """INSERT INTO training VALUES ($BUILD_ID,current_timestamp,'$BRANCH_NAME',$precision,'$model_name',$traintime,$testtime,'$CHANGE_AUTHOR','$sha')"""

            scp -r $WORKSPACE/src/predict/* ubuntu@172.31.36.254:$HOME/
            ssh 172.31.36.254
            touch prueba.txt
            exit

            '''


        }
   }

}


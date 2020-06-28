node('docker-slave') {
checkout scm
//   stage('Preparation') { // for display purposes
      // Get some code from a GitHub repository
      //git 'https://github.com/sergiobaquero/test1'
//  }
   stage('Build') {

      sh '''
          #!/bin/bash -xe
          rm $WORKSPACE/envvars || true

          commit_user=$(git show -s --pretty=%an)
          no_blank_commit_user=$(echo "$commit_user" | tr -d "[:space:]")
          echo "commit_user=\"$no_blank_commit_user\"" >> $WORKSPACE/envvars

          sha=$(git rev-parse HEAD)
          echo "sha=\"$sha\"" >> $WORKSPACE/envvars

          docker build -t sergiobaquero:trainingmodel .
      '''
   }
   stage('Train model') {
    withCredentials([usernamePassword(credentialsId: 'NexusUser', usernameVariable: 'USER', passwordVariable: 'PASS')]) {
      echo "Running ${env.BUILD_ID} on ${env.JENKINS_URL}"
      sh '''#!/bin/bash -xe

            start=`date +%s`
            . $WORKSPACE/envvars

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

            source_file=`cat .source_file.txt`
            echo "source_file=\"$source_file\"" >> $WORKSPACE/envvars
      '''
       }
    }
    stage('Test model') {
     withCredentials([usernamePassword(credentialsId: 'NexusUser', usernameVariable: 'USER', passwordVariable: 'PASS')]) {
      echo "Running ${env.BUILD_ID} on ${env.JENKINS_URL}"
      sh '''#!/bin/bash -xe

            start=`date +%s`

            . $WORKSPACE/envvars

            curl -v -u $USER:$PASS -X GET http://172.31.7.247:8081/repository/models/$model_name/$BRANCH_NAME/$sha/$model_name.pkl --output $model_name.pkl

            docker rm -f test || true
            docker run --name test  -v "$(pwd)":/code sergiobaquero:trainingmodel python3 ./src/test/test.py
            docker rm test

            precision=`cat .accuracy.txt`
            echo "precision=\"$precision\"" >> $WORKSPACE/envvars

            end=`date +%s`
            testtime=$((end-start))

            echo "testtime=\"$testtime\"" >> $WORKSPACE/envvars

        '''
    }
   }
      stage('Insert Database') {
        withCredentials([string(credentialsId: 'postgres_insert_user', variable: 'USER')]) {
            sh '''
            . $WORKSPACE/envvars

            if [ -z "$CHANGE_AUTHOR" ];
            then
              CHANGE_AUTHOR=$commit_user
            fi

            psql -h 172.31.7.247 -U $USER -d postgres -c """INSERT INTO training VALUES ($BUILD_ID,current_timestamp,'$BRANCH_NAME',$precision,'$model_name','$source_file',$traintime,$testtime,'$CHANGE_AUTHOR','$sha')"""

            '''
        }
   }
   stage('Deploy') {
            sh '''
            . $WORKSPACE/envvars
            ssh-keygen -f "/home/ubuntu/.ssh/known_hosts" -R "172.31.7.246"
            ssh ubuntu@172.31.7.246 mkdir $HOME/$model_name || true
            scp -pr $WORKSPACE/src/predict/* ubuntu@172.31.7.246:$HOME/$model_name

            #Los ficheros Dockerfile y boostrap.sh estan en la imagen de aplicaciones. Solo se copia a la carpeta del proyecto,
            #por si conviven varias aplicaciones desplegadas

            ssh ubuntu@172.31.7.246 cp Dockerfile $HOME/$model_name
            ssh ubuntu@172.31.7.246 cp boostrap.sh $HOME/$model_name
            ssh ubuntu@172.31.7.246 cp start.sh $HOME/$model_name
            ssh ubuntu@172.31.7.246 sh $HOME/$model_name/start.sh http://172.31.7.247:8081/repository/models/$model_name/$BRANCH_NAME/$sha/$model_name.pkl $HOME/$model_name/

            '''
   }

}


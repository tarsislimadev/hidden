FROM tmvdl/android:app

WORKDIR /app

RUN cordova create hidden com.brtmvdl.hidden hidden

WORKDIR /app/hidden

COPY www/html www

RUN cordova platform add android

RUN cordova build android

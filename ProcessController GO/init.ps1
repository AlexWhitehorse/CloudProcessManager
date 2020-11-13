mkdir weberr/bin
mkdir tmp

$progresspreferenceTmp = $progresspreference
$progresspreference = 'silentlyContinue'
#Invoke-WebRequest https://www.learningcontainer.com/wp-content/uploads/2020/05/sample-mp4-file.mp4 -OutFile media/example.mp4
Invoke-WebRequest https://ffmpeg.zeranoe.com/builds/win64/static/ffmpeg-20200628-4cfcfb3-win64-static.zip -OutFile tmp/ffmpeg.zip
$progresspreference = $progresspreferenceTmp
Expand-Archive -LiteralPath tmp/ffmpeg.zip -DestinationPath tmp/ffmpeg -Force
Copy-Item tmp/ffmpeg/*/bin/* weberr/bin/
Remove-Item tmp -Recurse -Force

$newpath = "$env:path;"+(Get-Location).Path+"\weberr\bin"
setx path $newpath -m

pause 
const Q = require('q')
const path = require('path')
const multer = require('multer')
const express = require('express')
const app = express()

app.use(express.static(path.resolve(__dirname, './frontend/')))

app.get('/', (req, res) => {
    res.sendFile(path.resolve(__dirname, './frontend/index.html'))
})

app.get('/download/apk', (req, res) => {
    res.download(path.resolve(__dirname, './slifit.apk'))
})

/* Create new image */
app.post('/upload/:filename', function(req, res, next) {
    upload(req, res).then(function (file) {
        res.json(file);
    }, function (err) {
        res.status(500).send(err);
    });
});

const upload = (req, res) => {
    const  deferred = Q.defer();
    const storage = multer.diskStorage({
      // 서버에 저장할 폴더
      destination: (req, file, cb) => {
        cb(null, './uploads');
      },
  
      // 서버에 저장할 파일 명
      filename: (req, file, cb) => {
        file.uploadedFile = {
          name: req.params.filename,
          ext: file.mimetype.split('/')[1]
        };
        cb(null, file.uploadedFile.name + '.' + file.uploadedFile.ext);
      }
    });
  
    const upload = multer({ storage: storage }).single('file');
    upload(req, res, (err) => {
      if (err) deferred.reject();
      else deferred.resolve(req.file.uploadedFile);
    });
    return deferred.promise;
  };

app.listen(8080)
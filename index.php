<?php

// GIF applications: gifsicle, convert
$gifApp = "gifsicle";

session_start();

if (isset($_GET['a']) && $_GET['a'] == "gifverse") {
    if (!file_exists("tmp")) {
        mkdir("tmp");
    }
    if (!file_exists("gifverses")) {
        mkdir("gifverses");
    }
    if (isset($_POST['url']) || isset($_GET['url'])) {
        if (isset($_GET['url'])) {
            $_POST['url'] = $_GET['url'];
        }
        $tmp_name = "/tmp/" . str_replace(" ", "", sha1(microtime() . date("U")));
        $name = preg_replace("/^.*\/(.*\.gif).*$/", "\${1}", $_POST['url']);
        file_put_contents($tmp_name, file_get_contents($_POST['url']));
        $_FILES['file']['name'] = $name;
        $_FILES['file']['tmp_name'] = $tmp_name;
        $_FILES['file']['size'] = filesize($tmp_name);
    }
    foreach ($_FILES as $type=>$f) {
        $fileName = $f['name'];
        if (!preg_match("/\.gif$/i", $fileName)) {
            continue;
        }
        $tmpFile = $f['tmp_name'];
        if (intval($f['size']) > 0 && intval($f['size']) < 15000000) {
            $orgFile = sha1(date("U") . microtime() . $fileName) . ".gif";
            $revFile = "rev.{$orgFile}";
            $comFile = "c{$orgFile}";
            copy($tmpFile, "tmp/{$orgFile}"); 
            $pwd = getcwd();
            chdir("tmp");

            if ($gifApp == "gifsicle") {
                exec("gifsicle --explode {$orgFile}");
                $gifs = glob("{$orgFile}.*");
                $r_gifs = array_reverse($gifs);
                foreach ($r_gifs as $gif) {
                    $cmd .= " {$gif} ";
                }
                $cmd = "gifsicle {$orgFile} {$cmd} > {$comFile}";
                exec($cmd);
                foreach ($r_gifs as $gif) {
                    unlink($gif);
                }
            } else if ($gifApp == "convert") {
                exec("convert {$orgFile} -reverse {$revFile}");
                exec("convert -delay 0 {$orgFile} {$revFile} -loop 0 {$comFile}");
                unlink($revFile);
            } else {
                exec("convert {$orgFile} -reverse {$revFile}");
                exec("convert -delay 0 {$orgFile} {$revFile} -loop 0 {$comFile}");
                unlink($revFile);
            }
            unlink($orgFile);
            rename($comFile, "../gifverses/{$comFile}");
            chdir($pwd);

        }
    }
    header("Location:{$_SERVER['PHP_SELF']}?gif=" . urlencode($comFile) . "#bottom");
    exit();
}

$gifverseIMG = "";
if (isset($_GET['gif']) && file_exists("gifverses/{$_GET['gif']}")) {
    $gifverseIMG = "<img src=\"gifverses/{$_GET['gif']}\" alt=\"gifverse\" />"; 
}

$html .= <<<eof
<!DOCTYPE html>
<html>
    <head>
        <meta charset="utf-8" />
        <title>GIFverse</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no" />
        <link type="text/css" rel="stylesheet" href="cdn/js/bootstrap/3.0.0/css/bootstrap.min.css" />
        <link type="text/css" rel="stylesheet" href="cdn/css/siamnet/default.css" />
    </head>
    <body>
        <div class="container">
            <header class="container header">
                <h1 class="heading">GIFverse</h1>
            </header>
            <article class="container">
                <div class="panel panel-primary">
                    <div class="panel-heading">Create a seamless GIF</div>
                    <div class="panel-body">
                        <form role="form" enctype="multipart/form-data" method="post" action="index.php?a=gifverse">
                            <div class="form-group">
                                <label for="gif">Upload a GIF</label>
                                <input class="form-control" type="file" name="gif" id="gif" />
                                <br />
                                <label for="url">URL</label>
                                <input class="form-control" type="text" id="url" name="url" placeholder="Full URL to GIF" />
                            </div>
                            <button type="submit" class="btn btn-primary">create</button>
                        </form>
                    </div>
                </div>
                <div class="container">
                    <p><a href="https://github.com/wsams/gifverse">Powered by gifverse</a></p>
                </div>
                <br />
                <div id="gifversed">{$gifverseIMG}</div>
                <br /><br /><br />
                <a name="bottom"></a>
            </article>
        </div>
        <script src="cdn/js/jquery/1.10.2/jquery-1.10.2.min.js"></script>
        <script src="cdn/js/bootstrap/3.0.0/js/bootstrap.min.js"></script>
        <script src="cdn/js/siamnet/default.js"></script>
        <script type="text/javascript">
            $(document).ready(function() {
                $("#url").focus();
            });
        </script>
    </body>
</html>
eof;

print($html);

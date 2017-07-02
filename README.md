gifverse
========

This is a simple but useful app for ridding the world of choppy GIFs. Do you dislike GIFs that don't loop seamlessly, toss them into the gifverse and they come out seamless.

Check out a demo. [https://vimeo.com/94618868](https://vimeo.com/94618868)

Chrome bookmarklet that will create a gifverse for any gif opened in a browser window. Just create a Chrome bookmark with the following `URL:`. Now all you have to do is open a gif in a window and click the bookmark. Make sure you're not on an HTML page containing the gif - you must be viewing it directly in the browser. i.e. `Open Image in New Tab`

```
javascript:function ue(u){u=encodeURIComponent(u);u=u.replace("+","+");u=u.replace("/","/");return u;}u=ue(location.href);t=ue(document.title);b="https://zoopaz.io/gifverse/index.php?a=gifverse&url="+u;window.location=b;
```

INSTALL
=======
This application can use one of two image applications to create the animated GIFs: `convert` from ImageMagick or the `gifsicle` program.

Open `index.php` and edit `$gifApp`. Set to one of `convert` or `gifsicle`.

Install one of the applications.

    sudo apt-get install gifsicle

    sudo apt-get install imagemagick

Open `index.php` in a browser. Upload a GIF and it's instantly gifversed.

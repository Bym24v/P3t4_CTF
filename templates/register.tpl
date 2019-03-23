
<!doctype html>
<html lang="es">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <meta name="description" content="">
    <meta name="author" content="@Bym24v">
    <!--<link rel="icon" href="../../../../favicon.ico">-->

    <title>P3t4 - CTF | Register</title>

    <!-- Bootstrap core CSS -->
    <link href="/static/css/bootstrap.min.css" rel="stylesheet">

    <!-- Custom styles for this template -->
    <link href="/static/css/signin.css" rel="stylesheet">
  </head>

  <body class="text-center">
    <form class="form-signin">
      <!--<img class="mb-4" src="../../assets/brand/bootstrap-solid.svg" alt="" width="72" height="72">-->
      
      <input type="email" maxlength="50" class="form-control br50 mt10" placeholder="Email" required autofocus>

      <input type="text" maxlength="30" class="form-control br50 mt10" placeholder="Usuario" required>
      
      <input type="password" maxlength="30" class="form-control br50 mt10 mb40" placeholder="Password" required>
      
      <div>

        <h6 class="text-muted">mov eax, 0xA y shl eax, 0x2</h6>
        <input type="text" class="form-control br50 mb20" placeholder="eax ?" required>
      
      </div>
      
      <button class="btn btn-lg btn-outline-primary btn-block br50 mt20 mb10" type="submit">Registrarse</button>
      <a class="text-muted" href="/login">Entrar</a>

      <!--<p class="mt-5 mb-3 text-muted">&copy; 2018-2019 CLS-CTF</p>-->

      <footer class="mastfoot mt-3">
        <div class="inner">
          <p class="text-muted mfooter">© 2018-2019 P3t4-CTF</p>
        </div>
      </footer>
      
    </form>
  </body>
</html>

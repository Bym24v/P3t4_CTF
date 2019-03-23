
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
    
	<form class="form-signin" actio="/register" method="POST">
      	
      	<input type="email" name="email" maxlength="50" class="form-control br50 mt10" placeholder="Email" required autofocus>

      	<input type="text" name="username" maxlength="30" class="form-control br50 mt10" placeholder="Usuario" required>
      
      	<input type="password" name="password" maxlength="30" class="form-control br50 mt10 mb40" placeholder="Password" required>
      
      	<h6 class="text-muted">mov eax, 0xA y shl eax, 0x2</h6>
        <input type="text" name="code" class="form-control br50 mb20" placeholder="eax" required>
      
      	<button class="btn btn-lg btn-outline-primary btn-block br50 mt20 mb10" type="submit">Registrarse</button>
      	<a class="text-muted" href="/login">Entrar</a>

      	<!--<p class="mt-5 mb-3 text-muted">&copy; 2018-2019 CLS-CTF</p>-->

      	<footer class="mastfoot mt-3">
        	<div class="inner">
          		<p class="text-muted mfooter">© 2018-2019 P3t4-CTF</p>
        	</div>
      	</footer>
    

		{% with messages  = get_flashed_messages(with_categories=true) %}
		{% if messages  %}

			{%- for category, message in messages  %}
				
				{% if category == "error" %}
					<div id="myAlert" class="alert alert-danger alert-dismissible fade show mt-5" role="alert">
						{{ message }}
						<button type="button" class="close" data-dismiss="alert" aria-label="Close">
							<span aria-hidden="true">&times;</span>
						</button>
					</div>
				{% endif %}

				{% if category == "require" %}
					<div id="myAlert" class="alert alert-warning alert-dismissible fade show mt-5" role="alert">
						{{ message }}
						<button type="button" class="close" data-dismiss="alert" aria-label="Close">
							<span aria-hidden="true">&times;</span>
						</button>
					</div>
				{% endif %}

				{% if category == "code" %}
					<div id="myAlert" class="alert alert-warning alert-dismissible fade show mt-5" role="alert">
						{{ message }}
						<button type="button" class="close" data-dismiss="alert" aria-label="Close">
							<span aria-hidden="true">&times;</span>
						</button>
					</div>
				{% endif %}

				{% if category == "done" %}
					<div id="myAlert" class="alert alert-success alert-dismissible fade show mt-5" role="alert">
						{{ message }}
						<button type="button" class="close" data-dismiss="alert" aria-label="Close">
							<span aria-hidden="true">&times;</span>
						</button>
					</div>
				{% endif %}

			{% endfor -%}

		{% endif %}
		{% endwith %}

    </form>

	<!-- Bootstrap core JavaScript
	================================================== -->
	<!-- Placed at the end of the document so the pages load faster -->
	<script src="https://code.jquery.com/jquery-3.3.1.slim.min.js" integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo" crossorigin="anonymous"></script>
	<script>window.jQuery || document.write('<script src="/public/js/jquery-slim.min.js"><\/script>')</script>
	<script src="/static/js/popper.min.js"></script>
	<script src="/static/js/bootstrap.min.js"></script>
  </body>
</html>

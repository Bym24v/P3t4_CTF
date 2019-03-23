
<!doctype html>
<html lang="es">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <meta name="description" content="">
    <meta name="author" content="@Bym24v">
    <!--<link rel="icon" href="../../../../favicon.ico">-->

    <title>P3t4 - CTF | Challenge</title>

    <!-- Bootstrap core CSS -->
    <link href="/static/css/bootstrap.min.css" rel="stylesheet">

    <!-- Custom styles for this template -->
    <link href="/static/css/dashboard.css" rel="stylesheet">
    <link href="/static/css/challenge.css" rel="stylesheet">
  </head>

  <body>
    <nav class="navbar navbar-dark fixed-top bg-dark flex-md-nowrap p-0 shadow">
      <a class="navbar-brand col-sm-12 col-md-12 mr-0" href="/">P3t4 - CTF<span> beta</span></a>
      <span>Score: 0</span>
    </nav>

    <div class="container-fluid">

      	<div class="row">

        	<nav class="col-md-2 d-none d-md-block sidebar" style="width: 200px;">
				
				<!-- sidebar -->
				<div class="sidebar-sticky sideColor">

					<ul class="nav flex-column">
				
						<li class="nav-item">
							<a class="nav-link active" href="/challenges">
							<span data-feather="coffee"></span>Challenges</a>
						</li>

						<li class="nav-item">
							<a class="nav-link text-muted" href="/users">
							<span data-feather="users"></span>Usuarios</a>
						</li>

						<li class="nav-item">
							<a class="nav-link text-muted" href="/profile/234342424234">
							<span data-feather="user"></span>Perfil</a>
						</li>

						<li class="nav-item">
							<a class="nav-link text-muted" href="/">
							<span data-feather="log-out"></span>Salir</a>
						</li>
				
					</ul>
				</div>
        	</nav>

        	<main role="main" class="col-md-10 ml-sm-auto col-lg-10 px-4">
          		
				<div class="d-flex justify-content-between flex-wrap flex-md-nowrap align-items-center pt-3 pb-2 mb-3">
				</div>
            	<!-- rows -->
				<form>
					<div class="row col-lg-12">

						<div class="py-5 col-md-12 text-center">
							<h2>Sube tu propio reto</h2>
							<p class="lead">Se popular dentro de la plataforma, lee la documentación para saber de como realizarlo.</p>
						</div>

						
						<!-- send file -->
						<div class="row col-md-12 mt-4">
							
							<h3 class="text-muted">Titulo</h3>
							<div class="input-group mb-3">
								<input type="text" class="form-control" placeholder="Titulo">
							</div>

							<h3 class="text-muted mt-5">Archivo ZIP</h3>
							<div class="input-group mb-3">
								<div class="custom-file">
									<input type="file" class="custom-file-input">
									<label class="custom-file-label">Archivo</label>
								</div>
							</div>

							<h3 class="text-muted mt-5">Descripción</h3>
							<div class="input-group">
								<textarea class="form-control"></textarea>
							</div>

						</div>

						<hr class="mb-4">
						<button class="btn btn-primary btn-lg btn-block mt-5" type="submit">ENVIAR</button>
					</div>
				</form>

        	</main> <!-- end main -->
     	</div>

    </div> <!-- end container-fluit -->

    <!-- Bootstrap core JavaScript
    ================================================== -->
    <!-- Placed at the end of the document so the pages load faster -->
    <script src="https://code.jquery.com/jquery-3.3.1.slim.min.js" integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo" crossorigin="anonymous"></script>
    <script>window.jQuery || document.write('<script src="../../assets/js/vendor/jquery-slim.min.js"><\/script>')</script>
    <script src="/static/js/popper.min.js"></script>
    <script src="/static/js/bootstrap.min.js"></script>

    <!-- Icons -->
    <script src="https://unpkg.com/feather-icons/dist/feather.min.js"></script>
    <script>
      feather.replace()
    </script>

    <script>
      $(function () {
        $('[data-toggle="tooltip"]').tooltip()
      })

    </script>
    
  </body>
</html>

<!doctype html>
<html lang="es">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <meta name="description" content="">
    <meta name="author" content="@Bym24v">
    <!--<link rel="icon" href="../../../../favicon.ico">-->

    <title>P3t4 - CTF | Profile</title>

    <!-- Bootstrap core CSS -->
    <link href="/static/css/bootstrap.min.css" rel="stylesheet">

    <!-- Custom styles for this template -->
    <link href="/static/css/dashboard.css" rel="stylesheet">
    <link href="/static/css/challenge.css" rel="stylesheet">
  </head>

  <body>
    <nav class="navbar navbar-dark fixed-top bg-dark flex-md-nowrap p-0 shadow">
      <a class="navbar-brand col-sm-12 col-md-12 mr-0" href="/">P3t4 - CTF</a>
    </nav>

    <div class="container-fluid">

      <div class="row">

		<!-- sidebar -->
        <nav class="col-md-2 d-none d-md-block sidebar" style="width: 200px;">
        	
			<!-- sidebar -->
          	<div class="sidebar-sticky sideColor">
            	<ul class="nav flex-column">
              
					<li class="nav-item">
						<a class="nav-link text-muted" href="/challenges">
						<span data-feather="coffee"></span>Challenges</a>
					</li>

					<li class="nav-item">
						<a class="nav-link text-muted" href="/users">
						<span data-feather="users"></span>Usuarios</a>
					</li>

					<li class="nav-item">
						<a class="nav-link active" href="/profile/234342424234">
						<span data-feather="user"></span>Perfil</a>
					</li>

					<li class="nav-item">
						<a class="nav-link text-muted" href="/">
						<span data-feather="log-out"></span>Salir</a>
					</li>
              
            	</ul>
          </div> <!-- end sidebar -->

        </nav>

        <main role="main" class="col-md-10 ml-sm-auto col-lg-10 px-4">

          	<!--<div class="d-flex justify-content-between flex-wrap flex-md-nowrap align-items-center pt-3 pb-2 mb-3">-->
            
        	<!-- rows -->
            <div class="row col-lg-12">

            	<div class="py-5 col-md-12 text-center">
					<!-- img -->
            		<img class="d-block mx-auto mb-4" src="https://cactusthemes.com/blog/wp-content/uploads/2018/01/tt_avatar_small.jpg" alt="" width="72" height="72" style="border-radius: 50px;">
                	
					<h2>Perfil de Usuario</h2>
                	<p class="lead">Aqui podras cambiar los datos de usuario.</p>
              	</div>

              	<div class="row col-md-12">
                
                	<div class="col-md-12">

                  		<h4 class="mb-3">Datos de usuario</h4>
                  		
						<form class="needs-validation" novalidate>
                    
                    		<div class="mb-3">
                      			<label for="username">Usuario</label>
                        		<input type="text" class="form-control" id="username" placeholder="Username" value="" required>
                        	
								<div class="invalid-feedback" style="width: 100%;">Nombre de usuario requerido.</div>
                      		</div>
                    		
							<div class="mb-3">
								<label for="email">Correo</label>
								<input type="email" class="form-control" id="email" placeholder="you@example.com" value="paco@paco.com" required>
								<div class="invalid-feedback">Correo requerido.</div>
							</div>

							<div class="mb-3">
								<label for="pass">Contraseña</label>
								<input type="password" class="form-control" id="pass" value="1234567876543" required>
								<div class="invalid-feedback">
									Contraseña requerida.
								</div>
							</div>

							<div class="mb-3">
								<label for="address">Twitter <span class="text-muted">(Optional)</span></label>
								<input type="text" class="form-control" id="address" placeholder="Bym24v">
							</div>

							<div class="mb-3">
								<label for="address2">Telegram <span class="text-muted">(Optional)</span></label>
								<input type="text" class="form-control" id="address2" placeholder="Bym24v">
							</div>

                    		<hr class="mb-4">
                    		<button class="btn btn-primary btn-lg btn-block" type="submit">GUARDAR</button>
                  		</form>
              		</div>
            	</div>
          	</div>

        </main>
      </div>
    </div>

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
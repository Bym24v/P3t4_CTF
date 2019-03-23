
<!doctype html>
<html lang="es">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <meta name="description" content="">
    <meta name="author" content="@Bym24v">
    <!--<link rel="icon" href="../../../../favicon.ico">-->

    <title>P3t4 - CTF | Usuarios</title>

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
        <nav class="col-md-2 d-none d-md-block sidebar" style="width: 200px;">
          <!-- sidebar -->
          <div class="sidebar-sticky sideColor">
            <ul class="nav flex-column">
              
              <li class="nav-item">
                <a class="nav-link text-muted" href="/challenges">
                  <span data-feather="coffee"></span>
                  Challenges
                </a>
              </li>

              <li class="nav-item">
                <a class="nav-link active" href="/users">
                  <span data-feather="users"></span>
                  Usuarios
                </a>
              </li>

              <li class="nav-item">
                <a class="nav-link text-muted" href="/profile/234342424234">
                  <span data-feather="user"></span>
                  Perfil
                </a>
              </li>

              <li class="nav-item">
                <a class="nav-link text-muted" href="/">
                  <span data-feather="log-out"></span>
                  Salir
                </a>
              </li>
              
            </ul>
          </div>
        </nav>

        <main role="main" class="col-md-10 ml-sm-auto col-lg-10 px-4">
          <div class="d-flex justify-content-between flex-wrap flex-md-nowrap align-items-center pt-3 pb-2 mb-3">
            
           <!-- rows -->
          <div class="row col-lg-12" style="margin-top: 25px;">

            <!-- send flag -->
            <div class="row col-md-12">

                <div class="py-5 col-md-12 text-center">
					<h2>Buscador de Usuarios</h2>
					<p class="lead">Aqui podras buscar a los usuarios de la plataforma.</p>
				</div>

              <div class="col-md-10">
                <input type="text" class="form-control" placeholder="Usuario" style="border-radius: 50px;">
              </div>

              <div class="col-md-2">
                <button class="btn btn-outline-primary" type="button" id="button-addon2" style="width: 100%; border-radius: 50px;">Buscar</button>
              </div>

            </div>

          
            <div class="table-responsive mt-5">
              
              <div class="col-md-12">
                <h2 class="mb-3">Usuarios</h2>

                <table class="table table-striped table">
                  
                  <tbody>
                    <tr>
                      <td class="td-50">1</td>
                      <td>pepe</td>
                    </tr>
                    <tr>
                      <td class="td-50">2</td>
                      <td>paco</td>
                    </tr>
                    <tr>
                      <td class="td-50">3</td>
                      <td>federico</td>
                    </tr>
                    <tr>
                      <td class="td-50">4</td>
                      <td>usebio</td>
                    </tr>
                    <tr>
                      <td class="td-50">5</td>
                      <td>Jhon</td>
                    </tr>
                    <tr>
                      <td class="td-50">6</td>
                      <td>langosta</td>
                    </tr>
                  </tbody>
                </table>
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
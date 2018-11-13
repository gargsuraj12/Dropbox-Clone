
    <script src="static/js/jquery-2.2.3.min.js"></script>
    <script type="text/javascript" src="static/js/popper.min.js"></script>
    <script src="static/js/bootstrap.min.js"></script>
    <script type="text/javascript" src="static/js/mdb.min.js"></script>

      <form action = "/opendirectory" method = "POST">
            
            <input type="text" name="userId" value="{{UserDetails.userid}}" style="display:none;">

            <input type="text" name="folderId" value="{{UserDetails.currentFolderId}}" style="display:none;">

            <button type="submit" class="btn btn-link float-left" >
              <div align="left">
                {%print items.filename%}
             </div>
           </button> 
          </form> 


import os

print os.urandom(24)
UserDetails.homeFolderId

<a class="nav-link active" 
        href="/index/{{UserDetails.userid}}/{{UserDetails.homeFolderId}}">
      <span data-feather="home"></span>
      <br><br>
       Home
    </a>

{% block search %}

    <form class="form-inline" action = "{{url_for('search')}}" method = "POST">
    <input name ="fileName" type="text" class=" form-control form-control-dark w-70" placeholder="Search" aria-label="Search" aria-describedby="button-addon2"/>
    <div class="input-group-append">
      <button class="btn btn-outline-default waves-effect" type="submit" id="button-addon2">
      <i class="fa fa-search fa-sm pr-2" aria-hidden="true"></i>
        Search</button>
    </div>
    </form>

{% endblock %}


    <nav class="navbar navbar-dark sticky-top bg-primary flex-md-nowrap p-0">
      {% block icon %}{% endblock %}
        <div class="float-left">
              
              {% block search %}{% endblock %}

        </div>
      <ul class="navbar-nav px-3">
        <li class="nav-item text-nowrap">
          {% block signOut %}{% endblock %}
        </li>
      </ul>
    </nav>



<input type="text" id="inputLGEx" class="form-control form-control-lg">

<a class="navbar-brand col-sm-3 col-md-2 mr-0" 
      href = "{{url_for('index',folderId = UserDetails.HomeFolderId)}}">
      Dropbox</a>



      {% if UserDetails.HomeFolderId == UserDetails.currentFolderId %}
  
    <h4 style="margin-left: 22%;margin-right:7%;">Home Folder:
     {% print UserDetails.HomeFolderId %}</h4>

    <h4 style="margin-left: 22%;margin-right:7%;">Current Folder: {% print UserDetails.currentFolderId %}</h4>

    <h4 style="margin-left: 22%;margin-right:7%;">Current Folder: Home </h4>

  {% else %}
  
    <h4 style="margin-left: 22%;margin-right:7%;">Current Folder: {% print UserDetails.currentFolderName %}</h4>

  {% endif %}





####################################################################################
issues

No result founds message display when search result is empty 

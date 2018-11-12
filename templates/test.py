
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




      {% if UserDetails.HomeFolderId == UserDetails.currentFolderId %}
  
    <h4 style="margin-left: 22%;margin-right:7%;">Home Folder:
     {% print UserDetails.HomeFolderId %}</h4>

    <h4 style="margin-left: 22%;margin-right:7%;">Current Folder: {% print UserDetails.currentFolderId %}</h4>

    <h4 style="margin-left: 22%;margin-right:7%;">Current Folder: Home </h4>

  {% else %}
  
    <h4 style="margin-left: 22%;margin-right:7%;">Current Folder: {% print UserDetails.currentFolderName %}</h4>

  {% endif %}



{% if items.filepermission|string == "0"|string %}
{% else %}
{% endif %}
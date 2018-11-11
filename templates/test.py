
    <script src="static/js/jquery-2.2.3.min.js"></script>
    <script type="text/javascript" src="static/js/popper.min.js"></script>
    <script src="static/js/bootstrap.min.js"></script>
    <script type="text/javascript" src="static/js/mdb.min.js"></script>

<!--           <form action = "/opendirectory" method = "POST">
            
            <input type="text" name="userId" value="{{UserDetails.userid}}" style="display:none;">

            <input type="text" name="folderId" value="{{UserDetails.currentFolderId}}" style="display:none;">

            <button type="submit" class="btn btn-link float-left" >
              <div align="left">
                {%print items.filename%}
             </div>
           </button> 
          </form>  --> 

import os

print os.urandom(24)
<grid drag="100 10" drop="top" bg="white" align="left" pad="0 20px">
 <% title %>
</grid>

<grid drag="28 75" drop="69 15" bg="white" style="border-radius:15px"/>

<grid drag="57 70" drop="3 15" align="topleft">

<% left %>

</grid>

<grid drag="40 71" drop="60 0" align="topright">

<% right %>

</grid>

<% content %>

<style>
.horizontal_dotted_line{
  border-bottom: 2px dotted gray;
} 
} 
</style>

<grid drag="94 0" drop="3 -6" class="horizontal_dotted_line">
</grid>

<grid drag="100 30" drop="0 64" align="bottomleft" pad="0 30px" >
<%? source %>
</grid>

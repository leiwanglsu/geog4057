<grid drag="100 10" drop="top" bg="white" align="top" pad="0 20px">
 <% title %>
 <!-- element style="font-size: 48px" -->
</grid>



<grid drag="45 70" drop="0 15" align="topleft">

<% left %>
<!-- element style="font-size: 30px" -->
</grid>

<grid drag="45 70" drop="60 15" align="topright">

<% right %>
<!-- element style="font-size: 30px" -->
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

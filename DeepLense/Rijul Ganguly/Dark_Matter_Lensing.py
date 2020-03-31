#!/usr/bin/env python
# coding: utf-8

# In[2]:




import autolens as al
import autolens.plot as aplt


# In[3]:


image_plane_grid = al.grid.uniform(
    shape_2d=(100, 100), pixel_scales=0.5, sub_size=1
)


# In[4]:


mass_profile = al.mp.SphericalNFW(centre=(0.0, 0.0), scale_radius=10)

lens_galaxy = al.Galaxy(redshift=0.5, mass=mass_profile)

light_profile = al.lp.SphericalSersic(
    centre=(0.0, 0.0), intensity=1.0, effective_radius=1.0, sersic_index=1.0
)

source_galaxy = al.Galaxy(redshift=1.0, light=light_profile)


# In[5]:


image_plane = al.Plane(galaxies=[lens_galaxy])


# In[6]:


deflections = image_plane.deflections_from_grid(grid=image_plane_grid)

print("deflection-angles of planes grid pixel 0:")
print(deflections.in_2d[0, 0, 0])
print(deflections.in_2d[0, 0, 0])

print("deflection-angles of planes grid pixel 1:")
print(deflections.in_2d[0, 1, 1])
print(deflections.in_2d[0, 1, 1])


# In[ ]:


aplt.plane.deflections_y(plane=image_plane, grid=image_plane_grid)

aplt.plane.deflections_x(plane=image_plane, grid=image_plane_grid)


# In[7]:


source_plane_grid = image_plane.traced_grid_from_grid(grid=image_plane_grid)
print("Traced source-plane coordinates of grid pixel 0:")
print(source_plane_grid.in_2d[0, 0, :])
print("Traced source-plane coordinates of grid pixel 1:")
print(source_plane_grid.in_2d[0, 1, :])


# In[8]:


source_plane = al.Plane(galaxies=[source_galaxy])


# In[9]:


aplt.plane.plane_grid(
    plane=image_plane, 
    grid=image_plane_grid, 
    plotter=aplt.Plotter(labels=aplt.Labels(title="Image-plane Grid")),
)

aplt.plane.plane_grid(
    plane=source_plane, 
    grid=source_plane_grid,
    plotter=aplt.Plotter(labels=aplt.Labels(title="Source-plane Grid")),
)


# In[10]:


aplt.plane.plane_grid(
    plane=source_plane,
    grid=source_plane_grid,
    axis_limits=[-0.1, 0.1, -0.1, 0.1],
    plotter=aplt.Plotter(labels=aplt.Labels(title="Source-plane Grid")),
)


# In[ ]:


aplt.plane.image_and_source_plane_subplot(
    image_plane=image_plane,
    source_plane=source_plane,
    grid=image_plane_grid,
    indexes=[
        range(0, 50),
        range(500, 550),
        [1350, 1450, 1550, 1650, 1750, 1850, 1950, 2050, 2150, 2250],
        [6250, 8550, 8450, 8350, 8250, 8150, 8050, 7950, 7850, 7750],
    ],
)


# In[11]:


aplt.plane.convergence(plane=source_plane, grid=source_plane_grid)


# In[12]:


aplt.plane.plane_image(
    plane=source_plane, 
    grid=source_plane_grid, 
    include=aplt.Include(grid=True)
)


# In[13]:


aplt.plane.plane_image(
    plane=source_plane, 
    grid=source_plane_grid, 
    include=aplt.Include(grid=False)
)


# In[ ]:


aplt.plane.image_and_source_plane_subplot(
    image_plane=image_plane,
    source_plane=source_plane,
    grid=image_plane_grid,
    include=aplt.Include(critical_curves=True, caustics=True),
)

aplt.plane.image_and_source_plane_subplot(
    image_plane=image_plane,
    source_plane=source_plane,
    grid=image_plane_grid,
    include=aplt.Include(critical_curves=False, caustics=False),
)


# In[ ]:





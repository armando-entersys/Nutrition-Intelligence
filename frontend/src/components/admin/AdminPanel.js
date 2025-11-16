/**
 * Admin Panel - Layout principal del panel de administración
 * Integra Dashboard, Gestión de Usuarios, Nutriólogos, Pacientes y Configuración
 */
import React, { useState } from 'react';
import {
  Box, Drawer, List, ListItem, ListItemIcon, ListItemText,
  ListItemButton, Toolbar, AppBar, Typography, IconButton,
  Divider, Avatar, Menu, MenuItem, Collapse
} from '@mui/material';
import {
  Dashboard as DashboardIcon, People, LocalHospital,
  PersonAdd, Settings, Logout, ExpandLess, ExpandMore,
  Menu as MenuIcon, PersonOutline
} from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';
import AdminDashboard from './AdminDashboard';
import UserManagement from './UserManagement';
import NutritionistManagement from './NutritionistManagement';
import PatientManagement from './PatientManagement';
import SystemSettings from './SystemSettings';

const drawerWidth = 260;

const AdminPanel = () => {
  const navigate = useNavigate();
  const [currentSection, setCurrentSection] = useState('dashboard');
  const [anchorEl, setAnchorEl] = useState(null);
  const [mobileOpen, setMobileOpen] = useState(false);
  const [usersMenuOpen, setUsersMenuOpen] = useState(false);

  const currentUser = JSON.parse(localStorage.getItem('nutrition_user') || '{}');

  const handleDrawerToggle = () => {
    setMobileOpen(!mobileOpen);
  };

  const handleMenuOpen = (event) => {
    setAnchorEl(event.currentTarget);
  };

  const handleMenuClose = () => {
    setAnchorEl(null);
  };

  const handleLogout = () => {
    localStorage.removeItem('nutrition_access_token');
    localStorage.removeItem('nutrition_refresh_token');
    localStorage.removeItem('nutrition_user');
    navigate('/auth/login');
  };

  const handleSectionChange = (section) => {
    setCurrentSection(section);
    if (mobileOpen) {
      setMobileOpen(false);
    }
  };

  const menuItems = [
    {
      id: 'dashboard',
      label: 'Dashboard',
      icon: <DashboardIcon />,
      component: <AdminDashboard />
    },
    {
      id: 'users',
      label: 'Gestión de Usuarios',
      icon: <People />,
      isParent: true,
      children: [
        {
          id: 'all-users',
          label: 'Todos los Usuarios',
          icon: <People />,
          component: <UserManagement />
        },
        {
          id: 'nutritionists',
          label: 'Nutriólogos',
          icon: <LocalHospital />,
          component: <NutritionistManagement />
        },
        {
          id: 'patients',
          label: 'Pacientes',
          icon: <PersonAdd />,
          component: <PatientManagement />
        }
      ]
    },
    {
      id: 'settings',
      label: 'Configuración',
      icon: <Settings />,
      component: <SystemSettings />
    }
  ];

  const renderContent = () => {
    // Check if it's a child item
    for (const item of menuItems) {
      if (item.children) {
        const childItem = item.children.find(child => child.id === currentSection);
        if (childItem) {
          return childItem.component;
        }
      } else if (item.id === currentSection) {
        return item.component;
      }
    }
    return <AdminDashboard />;
  };

  const drawer = (
    <Box>
      <Toolbar sx={{ bgcolor: 'primary.main', color: 'white' }}>
        <Typography variant="h6" noWrap component="div" sx={{ fontWeight: 'bold' }}>
          Panel Admin
        </Typography>
      </Toolbar>
      <Divider />
      <List>
        {menuItems.map((item) => (
          <React.Fragment key={item.id}>
            {item.isParent ? (
              <>
                <ListItemButton onClick={() => setUsersMenuOpen(!usersMenuOpen)}>
                  <ListItemIcon>{item.icon}</ListItemIcon>
                  <ListItemText primary={item.label} />
                  {usersMenuOpen ? <ExpandLess /> : <ExpandMore />}
                </ListItemButton>
                <Collapse in={usersMenuOpen} timeout="auto" unmountOnExit>
                  <List component="div" disablePadding>
                    {item.children.map((child) => (
                      <ListItemButton
                        key={child.id}
                        sx={{ pl: 4 }}
                        selected={currentSection === child.id}
                        onClick={() => handleSectionChange(child.id)}
                      >
                        <ListItemIcon>{child.icon}</ListItemIcon>
                        <ListItemText primary={child.label} />
                      </ListItemButton>
                    ))}
                  </List>
                </Collapse>
              </>
            ) : (
              <ListItemButton
                selected={currentSection === item.id}
                onClick={() => handleSectionChange(item.id)}
              >
                <ListItemIcon>{item.icon}</ListItemIcon>
                <ListItemText primary={item.label} />
              </ListItemButton>
            )}
          </React.Fragment>
        ))}
      </List>
    </Box>
  );

  return (
    <Box sx={{ display: 'flex' }}>
      {/* AppBar */}
      <AppBar
        position="fixed"
        sx={{
          width: { sm: `calc(100% - ${drawerWidth}px)` },
          ml: { sm: `${drawerWidth}px` },
        }}
      >
        <Toolbar>
          <IconButton
            color="inherit"
            edge="start"
            onClick={handleDrawerToggle}
            sx={{ mr: 2, display: { sm: 'none' } }}
          >
            <MenuIcon />
          </IconButton>
          <Typography variant="h6" noWrap component="div" sx={{ flexGrow: 1 }}>
            Nutrition Intelligence - Administración
          </Typography>
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
            <Typography variant="body2">
              {currentUser.first_name} {currentUser.last_name}
            </Typography>
            <IconButton onClick={handleMenuOpen} size="small">
              <Avatar
                sx={{ width: 32, height: 32, bgcolor: 'secondary.main' }}
              >
                {currentUser.first_name?.[0]}{currentUser.last_name?.[0]}
              </Avatar>
            </IconButton>
          </Box>
          <Menu
            anchorEl={anchorEl}
            open={Boolean(anchorEl)}
            onClose={handleMenuClose}
          >
            <MenuItem onClick={() => { navigate('/dashboard'); handleMenuClose(); }}>
              <PersonOutline sx={{ mr: 1 }} /> Mi Perfil
            </MenuItem>
            <Divider />
            <MenuItem onClick={handleLogout}>
              <Logout sx={{ mr: 1 }} /> Cerrar Sesión
            </MenuItem>
          </Menu>
        </Toolbar>
      </AppBar>

      {/* Drawer */}
      <Box
        component="nav"
        sx={{ width: { sm: drawerWidth }, flexShrink: { sm: 0 } }}
      >
        {/* Mobile drawer */}
        <Drawer
          variant="temporary"
          open={mobileOpen}
          onClose={handleDrawerToggle}
          ModalProps={{ keepMounted: true }}
          sx={{
            display: { xs: 'block', sm: 'none' },
            '& .MuiDrawer-paper': { boxSizing: 'border-box', width: drawerWidth },
          }}
        >
          {drawer}
        </Drawer>
        {/* Desktop drawer */}
        <Drawer
          variant="permanent"
          sx={{
            display: { xs: 'none', sm: 'block' },
            '& .MuiDrawer-paper': { boxSizing: 'border-box', width: drawerWidth },
          }}
          open
        >
          {drawer}
        </Drawer>
      </Box>

      {/* Main content */}
      <Box
        component="main"
        sx={{
          flexGrow: 1,
          p: 3,
          width: { sm: `calc(100% - ${drawerWidth}px)` },
          minHeight: '100vh',
          bgcolor: '#f5f5f5'
        }}
      >
        <Toolbar />
        {renderContent()}
      </Box>
    </Box>
  );
};

export default AdminPanel;

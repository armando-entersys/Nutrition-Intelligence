import React from 'react';
import { Breadcrumbs as MuiBreadcrumbs, Link, Typography, Box } from '@mui/material';
import { NavigateNext as NavigateNextIcon, Home as HomeIcon } from '@mui/icons-material';
import { motion } from 'framer-motion';

const MotionBox = motion(Box);

const Breadcrumbs = ({ items }) => {
  return (
    <MotionBox
      initial={{ opacity: 0, y: -10 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3 }}
      sx={{ py: 1 }}
    >
      <MuiBreadcrumbs
        separator={<NavigateNextIcon fontSize="small" sx={{ color: 'text.secondary' }} />}
        aria-label="breadcrumb"
        sx={{
          '& .MuiBreadcrumbs-separator': {
            mx: 0.5,
          },
        }}
      >
        {items.map((item, index) => {
          const isLast = index === items.length - 1;
          const isFirst = index === 0;

          if (item.onClick && !isLast) {
            return (
              <Link
                key={index}
                component="button"
                onClick={item.onClick}
                underline="hover"
                sx={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: 0.5,
                  color: 'primary.main',
                  fontWeight: 500,
                  fontSize: '0.875rem',
                  cursor: 'pointer',
                  border: 'none',
                  background: 'none',
                  padding: '4px 8px',
                  borderRadius: 1,
                  transition: 'all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1)',
                  '&:hover': {
                    bgcolor: 'primary.light',
                    color: 'primary.dark',
                    transform: 'translateY(-1px)',
                  },
                }}
              >
                {isFirst && <HomeIcon fontSize="small" />}
                {item.label}
              </Link>
            );
          }

          return (
            <Typography
              key={index}
              sx={{
                display: 'flex',
                alignItems: 'center',
                gap: 0.5,
                color: isLast ? 'text.primary' : 'text.secondary',
                fontWeight: isLast ? 600 : 500,
                fontSize: '0.875rem',
              }}
            >
              {isFirst && <HomeIcon fontSize="small" />}
              {item.label}
            </Typography>
          );
        })}
      </MuiBreadcrumbs>
    </MotionBox>
  );
};

export default Breadcrumbs;

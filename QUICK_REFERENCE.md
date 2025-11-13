# Quick Reference - Nutrition Intelligence

## 🚀 Inicio Rápido

### Ver Estado del Sistema
```bash
# Ver resumen del proyecto
cat PROJECT_SUMMARY.md

# Ver próximos pasos
cat NEXT_STEPS.md

# Ver estructura
tree -L 2
```

## 📁 Archivos Importantes Creados

1. **PROJECT_SUMMARY.md** - Resumen ejecutivo completo
2. **NEXT_STEPS.md** - Plan detallado para continuar
3. **README.md** - Overview del proyecto
4. **docs/** - 10 documentos técnicos completos

## ⚡ Comandos Más Usados

### Desarrollo
```bash
# Backend
cd backend
pip install -r requirements-dev.txt
pytest --cov=backend --cov-report=html

# Frontend  
cd frontend
npm test
npx playwright test

# Docker
docker-compose up -d
docker-compose logs -f
```

### Producción
```bash
# SSH a servidor
gcloud compute ssh prod-server --zone=us-central1-c

# Deploy
cd /srv/scram/nutrition-intelligence
git pull origin main
docker compose up -d --build

# Health check
./backend/scripts/health_check.sh
```

## 📊 URLs Importantes

- **Producción**: https://nutrition-intelligence.scram2k.com
- **API Docs**: https://nutrition-intelligence.scram2k.com/docs
- **GitHub**: [Tu repositorio]

## ✅ Checklist Pre-Lanzamiento

- [ ] Ejecutar tests completos
- [ ] Poblar base de datos con más alimentos
- [ ] Configurar Sentry
- [ ] Configurar Google Analytics
- [ ] Optimizar SEO
- [ ] Beta testing con 10 usuarios
- [ ] Documentar feedback
- [ ] ¡Lanzar!

## 🆘 Troubleshooting

### Error: Tests no corren
```bash
pip install -r requirements-dev.txt
pytest --version
```

### Error: Docker no inicia
```bash
docker-compose down
docker system prune -a
docker-compose up -d --build
```

### Error: Base de datos no conecta
```bash
docker-compose logs db
docker exec -it nutrition-intelligence-db psql -U nutrition_user
```

## 📞 Soporte

- Docs: Ver carpeta docs/
- Issues: GitHub Issues
- Email: soporte@ejemplo.com

---
**Versión**: 1.0.0 | **Status**: 🟢 Production Ready


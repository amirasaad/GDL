FROM solr:8.6.3-slim

EXPOSE 8983

COPY --chown=solr:solr ./compose/local/solr/drive/ /drive

CMD ["solr-precreate", "drive", "/drive"]

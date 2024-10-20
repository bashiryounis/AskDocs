#!/bin/sh

# Replace environment variables in the nginx configuration
envsubst < /etc/nginx/conf.d/default.conf > /etc/nginx/conf.d/default.conf.tmp
mv /etc/nginx/conf.d/default.conf.tmp /etc/nginx/conf.d/default.conf

# Start nginx
nginx -g 'daemon off;'
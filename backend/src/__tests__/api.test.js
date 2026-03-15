import express from 'express';
import request from 'supertest';
import { app } from '../index';

describe('Backend API Tests', () => {
  describe('Health Check', () => {
    test('GET /health should return 200', async () => {
      const response = await request(app).get('/health');
      expect(response.statusCode).toBe(200);
      expect(response.body).toHaveProperty('status', 'ok');
    });
  });

  describe('Authentication', () => {
    test('POST /api/v1/auth/register should create user', async () => {
      const response = await request(app)
        .post('/api/v1/auth/register')
        .send({
          email: 'test@example.com',
          password: 'password123',
          full_name: 'Test User'
        });
      expect(response.statusCode).toBe(201);
      expect(response.body).toHaveProperty('id');
    });

    test('POST /api/v1/auth/login should return token', async () => {
      const response = await request(app)
        .post('/api/v1/auth/login')
        .send({
          email: 'test@example.com',
          password: 'password123'
        });
      expect(response.statusCode).toBe(200);
      expect(response.body).toHaveProperty('token');
    });
  });

  describe('Campaigns', () => {
    test('GET /api/v1/campaigns should return empty array', async () => {
      const response = await request(app).get('/api/v1/campaigns');
      expect(response.statusCode).toBe(200);
      expect(Array.isArray(response.body)).toBe(true);
    });

    test('POST /api/v1/campaigns should create campaign', async () => {
      const response = await request(app)
        .post('/api/v1/campaigns')
        .set('Authorization', 'Bearer test-token')
        .send({
          name: 'Test Campaign',
          description: 'Test description'
        });
      expect(response.statusCode).toBe(201);
      expect(response.body).toHaveProperty('id');
    });
  });

  describe('Validation', () => {
    test('POST /api/v1/auth/register with invalid email should fail', async () => {
      const response = await request(app)
        .post('/api/v1/auth/register')
        .send({
          email: 'invalid-email',
          password: 'password123'
        });
      expect(response.statusCode).toBe(400);
    });

    test('POST /api/v1/auth/register with short password should fail', async () => {
      const response = await request(app)
        .post('/api/v1/auth/register')
        .send({
          email: 'test@example.com',
          password: 'short'
        });
      expect(response.statusCode).toBe(400);
    });
  });
});

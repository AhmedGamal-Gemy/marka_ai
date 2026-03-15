// Frontend test examples (Jest)

describe('Frontend Components', () => {
  describe('Login Component', () => {
    it('renders email input field', () => {
      const { getByLabelText } = render(<LoginForm />);
      const emailInput = getByLabelText(/email/i);
      expect(emailInput).toBeInTheDocument();
    });

    it('renders password input field', () => {
      const { getByLabelText } = render(<LoginForm />);
      const passwordInput = getByLabelText(/password/i);
      expect(passwordInput).toBeInTheDocument();
    });

    it('submits form with valid data', async () => {
      const mockLogin = jest.fn();
      render(<LoginForm onLogin={mockLogin} />);

      const emailInput = screen.getByLabelText(/email/i);
      const passwordInput = screen.getByLabelText(/password/i);
      const submitButton = screen.getByText(/login/i);

      await userEvent.type(emailInput, 'test@example.com');
      await userEvent.type(passwordInput, 'password123');
      await userEvent.click(submitButton);

      expect(mockLogin).toHaveBeenCalledWith({
        email: 'test@example.com',
        password: 'password123'
      });
    });
  });

  describe('Campaign List Component', () => {
    it('renders empty state when no campaigns', () => {
      render(<CampaignList campaigns={[]} />);
      expect(screen.getByText(/no campaigns/i)).toBeInTheDocument();
    });

    it('renders campaign items', () => {
      const campaigns = [
        { id: '1', name: 'Campaign 1', status: 'active' }
      ];
      render(<CampaignList campaigns={campaigns} />);
      expect(screen.getByText('Campaign 1')).toBeInTheDocument();
    });
  });

  describe('API Service', () => {
    it('fetches campaigns successfully', async () => {
      // Mock axios
      jest.spyOn(axios, 'get').mockResolvedValue({
        data: [
          { id: '1', name: 'Campaign 1' }
        ]
      });

      const result = await getCampaigns();
      expect(result).toEqual([
        { id: '1', name: 'Campaign 1' }
      ]);
    });

    it('handles API errors', async () => {
      jest.spyOn(axios, 'get').mockRejectedValue(new Error('Network error'));

      await expect(getCampaigns()).rejects.toThrow('Network error');
    });
  });
});

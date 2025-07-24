using System.ComponentModel.DataAnnotations;

namespace UserAuthMvc.Entities
{
    public class PasswordReset
    {
        [Key]
        public int Id { get; set; }

        [Required(ErrorMessage = "E-Mail is required.")]
        [EmailAddress(ErrorMessage = "Please enter a valid e-mail address.")]
        public string Email { get; set; }
       
        [Required(ErrorMessage = "Password is required.")]
        [StringLength(128, MinimumLength = 6, ErrorMessage = "The password can be at least 6 and at most 128 characters.")]
        public string Token { get; set; }
        public DateTime ExpiryDate { get; set; }
    }
}

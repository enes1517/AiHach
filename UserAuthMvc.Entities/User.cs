using System;
using System.ComponentModel.DataAnnotations;

namespace UserAuthMvc.Entities
{
    public class User
    {
        [Key]
        public int Id { get; set; }
        
        [Required(ErrorMessage ="Username is required")]
        [StringLength(50, ErrorMessage = "The Username can be up to 50 characters.")]

        public string UserName { get; set; }
        
        [Required(ErrorMessage = "E-Mail is required.")]
        [EmailAddress(ErrorMessage = "Please enter a valid e-mail address.")]
        public string Email { get; set; }
       
        [Required(ErrorMessage = "Password is required")]
        [StringLength(128, MinimumLength = 6, ErrorMessage = "The password can be at least 6 and at most 128 characters.")]
        public string PasswordHash { get; set; }
        public bool IsAdmin { get; set; } = false;
        [Required(ErrorMessage = "Password is required")]
        [StringLength(128, MinimumLength = 6, ErrorMessage = "The password can be at least 6 and at most 128 characters.")]
        public string? ResetToken { get; set; }
        public DateTime? ResetTokenExpiry { get; set; }
    }
}

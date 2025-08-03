using System;
using System.Collections.Generic;
using Microsoft.EntityFrameworkCore;

namespace UserAuthMvc.DAL.TempModels;

public partial class TempDbContext : DbContext
{
    public TempDbContext()
    {
    }

    public TempDbContext(DbContextOptions<TempDbContext> options)
        : base(options)
    {
    }

    public virtual DbSet<PasswordReset> PasswordResets { get; set; }

    public virtual DbSet<User> Users { get; set; }

    protected override void OnConfiguring(DbContextOptionsBuilder optionsBuilder)
#warning To protect potentially sensitive information in your connection string, you should move it out of source code. You can avoid scaffolding the connection string by using the Name= syntax to read it from configuration - see https://go.microsoft.com/fwlink/?linkid=2131148. For more guidance on storing connection strings, see https://go.microsoft.com/fwlink/?LinkId=723263.
        => optionsBuilder.UseSqlServer("Server=(localdb)\\mssqllocaldb;Database=UserAuthMvcDb;Trusted_Connection=True;");

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        modelBuilder.Entity<PasswordReset>(entity =>
        {
            entity.HasKey(e => e.Id).HasName("PK__Password__3214EC07EC9EC98F");

            entity.Property(e => e.Email).HasMaxLength(256);
            entity.Property(e => e.ExpiryDate).HasColumnType("datetime");
            entity.Property(e => e.Token).HasMaxLength(100);
        });

        modelBuilder.Entity<User>(entity =>
        {
            entity.HasKey(e => e.Id).HasName("PK__Users__3214EC0797CF9A45");

            entity.Property(e => e.Email).HasMaxLength(256);
            entity.Property(e => e.PasswordHash).HasMaxLength(256);
            entity.Property(e => e.ResetToken).HasMaxLength(100);
            entity.Property(e => e.ResetTokenExpiry).HasColumnType("datetime");
            entity.Property(e => e.UserName).HasMaxLength(100);
        });

        OnModelCreatingPartial(modelBuilder);
    }

    partial void OnModelCreatingPartial(ModelBuilder modelBuilder);
}

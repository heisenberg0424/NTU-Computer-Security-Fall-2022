import zipfile
z_info = zipfile.ZipInfo(r"/__init__.py")
z_file = zipfile.ZipFile("bad.zip", mode="w")
z_file.writestr(z_info, "print 'test'")
z_file.close()
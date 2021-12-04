[DllImport("User32.dll")]
public static extern IntPtr GetDC(IntPtr hwnd);

[DllImport("User32.dll")]
public static extern void ReleaseDC(IntPtr dc);

protected override void OnPaint(PaintEventArgs e)

{

SolidBrush b=new SolidBrush(Color.Red);
IntPtr desktopDC=GetDC(IntPtr.Zero);

Graphics g = Graphics.FromHdc(desktopDC);

g.FillEllipse(b,0,0,1024,768);

g.Dispose();

ReleaseDC(desktopDC);

}

import NextAuth,  { NextAuthOptions } from "next-auth"
const authOptions: NextAuthOptions = {
  // Configure one or more authentication providers
  providers: [],
}
const handler = NextAuth(authOptions);
export { handler as GET, handler as POST };
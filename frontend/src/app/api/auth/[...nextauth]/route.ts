import NextAuth from "next-auth"
export const authOptions = {
  // Configure one or more authentication providers
  providers: [],
}
export default NextAuth(authOptions)
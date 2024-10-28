import httpx
import base64
import urllib.parse
from typing import Dict, Tuple, List, Optional

from fastapi import HTTPException


class GitHubAPI:
    """Handles interactions with the GitHub API, including retrieving repository trees and file contents."""

    MAX_ENTRIES: int = 100000
    MAX_SIZE_MB: int = 7

    def __init__(self, github_repo_url: str, token: str) -> None:
        self.repo_title: str = self._get_repo_title(github_repo_url)
        self.token: str = token
        self.headers: Dict[str, str] = {
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {self.token}",
            "X-GitHub-Api-Version": "2022-11-28",
        }

    @staticmethod
    def _get_repo_title(github_url: str) -> Optional[str]:
        """Extracts the "owner/repository" format from a GitHub URL, returning it if valid, otherwise returning None."""
        parsed_url = urllib.parse.urlparse(github_url)
        parsed_path = parsed_url.path.split("/")
        return f"{parsed_path[1]}/{parsed_path[2]}" if len(parsed_path) > 2 else None

    async def _get_tree(
        self, branch: str = "main", recursive: bool = True
    ) -> List[Dict]:
        """Get the list of files and directories in the repository."""
        url: str = f"https://api.github.com/repos/{self.repo_title}/git/trees/{branch}"
        params: Dict[str, str] = {"recursive": "1" if recursive else "0"}

        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=self.headers, params=params)

        if response.status_code == 200:
            tree: List[Dict] = response.json().get("tree", [])

            if len(tree) > self.MAX_ENTRIES:
                raise HTTPException(
                    status_code=403,
                    detail=f"Exceeded the maximum number of entries: {self.MAX_ENTRIES}",
                )

            total_size: int = sum(
                item.get("size", 0) for item in tree if item["type"] == "blob"
            )
            if total_size > self.MAX_SIZE_MB * 1024 * 1024:
                raise HTTPException(
                    status_code=403,
                    detail=f"Exceeded the maximum size limit: {self.MAX_SIZE_MB} MB",
                )
            return tree
        else:
            raise HTTPException(
                status_code=response.status_code,
                detail=f"Failed to retrieve tree: {response.text}",
            )

    async def get_file_content(self, path: str) -> str:
        """Get the content of a file by its path."""
        url: str = f"https://api.github.com/repos/{self.repo_title}/contents/{path}"

        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=self.headers)

        if response.status_code == 200:
            content: str = response.json().get("content", "")
            return base64.b64decode(content).decode("utf-8")
        else:
            raise HTTPException(
                status_code=response.status_code,
                detail=f"Failed to retrieve file content for {path}: {response.text}",
            )

    async def get_all_files(self) -> Tuple[str, str]:
        """Get a list of all files and their contents in the repository."""
        file_list: Dict[str, str] = {}
        tree: List[Dict] = await self._get_tree()

        for item in tree:
            if item["type"] == "blob":
                file_path: str = item["path"]
                content: str = await self.get_file_content(file_path)
                file_list[file_path] = content

        file_paths_string: str = "\n".join(file_list.keys())
        file_contents_string: str = "\n".join(
            f"Content of {path}:\n{content}" for path, content in file_list.items()
        )

        return file_paths_string, file_contents_string
